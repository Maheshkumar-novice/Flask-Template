from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


def password_field(type='password'):
    validators = [
        DataRequired(),
        Length(min=8, max=50),
        Regexp(regex='(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,50}')
    ]

    if type == 'repeat_password':
        label = 'Repeat Password'
        validators.append(EqualTo('password'))
    else:
        label = 'Password'

    return PasswordField(label, validators=validators, description=label)
