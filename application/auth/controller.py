import json
import traceback
import uuid

import jwt
import requests
from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from application.auth.forms import (
    ForgotPasswordForm,
    ResetPasswordForm,
    SignInForm,
    SignUpForm,
)
from application.auth.google_auth_utils import get_google_provider_cfg
from application.auth.models import User
from config import Config
from database.resource import DBSession
from lib.email import EmailSender
from lib.flash import Flash


def signup():
    if not current_user.is_anonymous:
        return redirect(url_for('auth.user_home'))

    form = SignUpForm()

    if form.validate_on_submit():
        with DBSession() as session, session.begin():
            user = session.scalar(select(User).where(
                User.email == form.email.data))

            if user is not None:
                Flash.error('User already exists.')
                return redirect(url_for('auth.signin'))

            user = User(
                id=uuid.uuid4(),
                name=form.name.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                is_active=False
            )
            session.add(user)
        Flash.success(
            'User creation success. Please check your mail to activate & signin.')
        EmailSender(form.email.data).send_activation_email()
        return redirect(url_for('auth.signin'))
    else:
        return render_template('signup.html', form=form)


def signin():
    if not current_user.is_anonymous:
        return redirect(url_for('auth.user_home'))

    form = SignInForm()

    if form.validate_on_submit():
        with DBSession() as session:
            user = session.scalar(select(User).filter_by(
                email=form.email.data
            ))

            if user and user.is_google_user:
                Flash.error('Please signin with google for this email.')
            elif (not user) or (not check_password_hash(user.password_hash, form.password.data)):
                Flash.error('Please check email/password.')
            elif (not user.is_active) or (user.is_deleted):
                Flash.error(
                    'User does not exist or inactive. Please contact support.')
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('auth.user_home'))
            return redirect(url_for('auth.signin'))
    else:
        return render_template('signin.html', form=form)


def signin_with_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = Config.OAUTHCLIENT.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)


def signin_with_google_callback():
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    token_url, headers, body = Config.OAUTHCLIENT.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    Config.OAUTHCLIENT.parse_request_body_response(
        json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = Config.OAUTHCLIENT.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        user_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        user_name = userinfo_response.json()['given_name']
    else:
        Flash.error('User email not available or not verified by Google.')
        return redirect(url_for('auth.login'))

    with DBSession() as session, session.begin():
        user = User(
            id=unique_id,
            name=user_name,
            email=user_email,
            profile_picture_url=picture,
            is_google_user=True
        )

        existing_user = session.scalar(
            select(User).where(User.email == user.email))

        if existing_user is None:
            session.add(user)
        elif not existing_user.is_google_user:
            Flash.error('Please sign in with your email and password.')
            redirect(url_for('auth.signin'))

        login_user(user, remember=True)
        return redirect(url_for('index'))


def verify_email(token):
    try:
        data = jwt.decode(
            token, current_app.config['SECRET_KEY'], algorithms='HS256')
    except Exception as e:
        current_app.logger.error(
            f'JWT Error: {str(e)} {traceback.format_exc()}')
        Flash.error('Please try again.')
        return redirect(url_for('auth.signin'))

    email = data['email']

    with DBSession() as session, session.begin():
        existing_user = session.scalar(
            select(User).where(User.email == email))

        if existing_user:
            existing_user.is_active = True
        else:
            Flash.error('Invalid activation link.')
            return redirect(url_for('auth.signup'))

        session.add(existing_user)
        Flash.success('User activation success. Please login to continue.')
        return redirect(url_for('auth.signin'))


def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        with DBSession() as session, session.begin():
            user = session.scalar(select(User).where(
                User.email == form.email.data))

            Flash.info('Password reset mail sent.')

            if user:
                EmailSender(form.email.data).send_password_reset_mail()

            return redirect(url_for('index'))
    else:
        return render_template('forgot_password.html', form=form)


def reset_password(token):
    form = ResetPasswordForm()

    if form.validate_on_submit():
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms='HS256')
        except Exception as e:
            current_app.logger.error(
                f'JWT Error: {str(e)} {traceback.format_exc()}')
            Flash.error('Please try again.')
            return redirect(url_for('auth.forgot_password'))

        email = data['email']

        with DBSession() as session, session.begin():
            existing_user = session.scalar(
                select(User).where(User.email == email))

            if existing_user:
                existing_user.password_hash = generate_password_hash(
                    form.password.data)
            else:
                Flash.error('Invalid reset link.')
                return redirect(url_for('index'))

            session.add(existing_user)
            Flash.success('Reset password success. Please login to continue.')
            return redirect(url_for('auth.signin'))
    else:
        return render_template('reset_password.html', form=form, token=token)


@login_required
def user_home():
    return render_template('user_home.html', name=current_user.name)


@login_required
def signout():
    logout_user()
    Flash.success('Logged out.')
    return redirect(url_for('index'))
