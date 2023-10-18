import os

from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient
from datetime import timedelta

load_dotenv()


class Config():
    DB_URL = os.environ['DB_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
    WTF_CSRF_ENABLED = True if os.environ.get(
        'WTF_CSRF_ENABLED') == 'True' else False
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = os.environ.get('GOOGLE_DISCOVERY_URL')
    OAUTHCLIENT = WebApplicationClient(GOOGLE_CLIENT_ID)
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.environ.get('REMEMBER_COOKIE_DURATION_DAYS', 1)))
    REMEMBER_COOKIE_SECURE = os.environ['REMEMBER_COOKIE_SECURE']
    REMEMBER_COOKIE_SAMESITE = os.environ['REMEMBER_COOKIE_SAMESITE']
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    SENDGRID_SENDER_EMAIL = os.environ['SENDGRID_SENDER_EMAIL']
    