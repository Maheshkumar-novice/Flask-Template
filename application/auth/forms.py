from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, StringField
from wtforms.validators import DataRequired, Email

from lib.form import password_field


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], description='Name')
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    password = password_field()
    repeat_password = password_field(type='repeat_password')


class SignInForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    password = password_field()
    remember_me = BooleanField('Remember Me', default=False)


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[
                       DataRequired(), Email()], description='Email')


class ResetPasswordForm(FlaskForm):
    password = password_field()
    repeat_password = password_field(type='repeat_password')
