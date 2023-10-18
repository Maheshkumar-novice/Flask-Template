from flask import Blueprint

from application.auth.controller import (
    forgot_password,
    reset_password,
    signin,
    signin_with_google,
    signin_with_google_callback,
    signout,
    signup,
    user_home,
    verify_email,
)

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/')


auth_blueprint.add_url_rule(rule='/signup',
                            view_func=signup,
                            endpoint='signup',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/signin',
                            view_func=signin,
                            endpoint='signin',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/signin/google',
                            view_func=signin_with_google,
                            endpoint='signin_with_google',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/signin/google/callback',
                            view_func=signin_with_google_callback,
                            endpoint='signin_with_google_callback',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/verify-email/<token>',
                            view_func=verify_email,
                            endpoint='verify_email',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/forgot-password',
                            view_func=forgot_password,
                            endpoint='forgot_password',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/reset-password/<token>',
                            view_func=reset_password,
                            endpoint='reset_password',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/user-home',
                            view_func=user_home,
                            endpoint='user_home',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/signout',
                            view_func=signout,
                            endpoint='signout',
                            methods=['GET'])
