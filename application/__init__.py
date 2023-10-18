from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user

from config import Config

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.signin'
    login_manager.refresh_view = 'auth.signin'
    login_manager.session_protection = 'strong'

    from application.auth.models import User
    from database.resource import DBSession

    @login_manager.user_loader
    def load_user(user_id):
        return DBSession().get(User, user_id)

    @app.teardown_appcontext
    def remove_session(_exception):
        DBSession.remove()

    from application.auth.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def index():
        if not current_user.is_anonymous:
            return redirect(url_for('auth.user_home'))
        return render_template('index.html')
    
    @app.context_processor
    def context_variables():
        if request.endpoint == 'index':
            navbar_type = 'home'
        else:
            navbar_type = 'other'

        return {'navbar_type': navbar_type}

    return app
