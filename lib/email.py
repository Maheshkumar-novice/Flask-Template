from time import time

import jwt
from flask import current_app, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGridMailSender:
    @staticmethod
    def send(email, html):
        SendGridAPIClient(current_app.config['SENDGRID_API_KEY']).send(
            Mail(
                from_email=current_app.config['SENDGRID_SENDER_EMAIL'],
                to_emails=email,
                subject='Text Gen: Activate Your Account',
                html_content=html
            )
        )


class EmailSender:
    def __init__(self, email) -> None:
        self.email = email
        self.mail_client = SendGridMailSender

    def send_activation_email(self):
        token = jwt.encode({'email': self.email,
                            'exp': time() + 300},
                           key=current_app.config['SECRET_KEY'],
                           algorithm='HS256')
        url = url_for('auth.verify_email', token=token, _external=True)

        html = f'''
        <h1>Text Gen</h1>
        <p>Please activate your account to use our services. Click on the link below.</p>

        <a href='{url}'>Activate</a> 
        '''
        self.mail_client.send(self.email, html)

    def send_password_reset_mail(self):
        token = jwt.encode({'email': self.email,
                            'exp': time() + 300},
                           key=current_app.config['SECRET_KEY'],
                           algorithm='HS256')
        url = url_for('auth.reset_password', token=token, _external=True)
        html = f'''
        <h1>Text Gen</h1>
        <p>To reset your password, please click on the link below.</p>

        <a href='{url}'>Reset</a> 
        '''
        self.mail_client.send(self.email, html)
