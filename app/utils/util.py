#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains some useful and essential function utilities."""

# bulit-in modules
import re
import hashlib
from datetime import datetime, timedelta
from io import StringIO

# third-party modules
import jwt
import markdown2
from flask import url_for, render_template
from flask_babel import lazy_gettext as _l
from flask_mail import Message
from flask_restx import ValidationError
from itsdangerous import URLSafeTimedSerializer
from markdown import Markdown
from twilio.rest import Client
from password_strength import PasswordPolicy
import phonenumbers

# own modules
from app.app import mail
from app.modules.user.user import User
from app import db
from app.modules.user.blacklist import BlacklistToken
from app.settings.config import BaseConfig

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


client = Client(username=BaseConfig.TWILIO_ACCOUNT_SID, password=BaseConfig.TWILIO_AUTH_TOKEN)


def encode_file_name(filename):
    ''' Encode the filename (without extension).

    Args:
        filename: The filename.

    Returns:
         The encoded filename.
    '''

    encoded = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return encoded


def generate_conformation_token(email):
    """ Confirmation email token

    Args:
        email: The email used to generate confirmation token.

    Return:

    """
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECURITY_SALT)


def confirm_token(token, expirations=3600):
    """ Confirm token.

    Args:
        token: The token to confirm.

    Returns
        expirations: The expiration time.

    Returns:
         email if success and None vice versa.
    """

    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=BaseConfig.SECURITY_SALT, max_age=expirations)
        return email
    except Exception as e:
        print(e.__str__())
        return None


def send_email(to, subject, template):
    """ Send an email.

    Args:
        to: The email-address to send to.
        subject: The subject of the email.
        template: The template to generate email.

    Return:
    """
    
    msg = Message(subject, sender=BaseConfig.MAIL_USERNAME, recipients=[to], html=template)
    mail.send(msg)


def send_confirmation_email(to):
    """ Send a confirmation email to the registered user.

    Args:
        to: The email address to send to.

    Return:
    """
    
    token = generate_conformation_token(email=to)
    confirm_url = url_for('auth_confirmation_email', token=token, _external=True)
    html = render_template('confirmation.html', confirm_url=confirm_url)
    send_email(to, 'Xác nhận đăng ký', html)


def send_password_reset_email(to):
    """ Send a password reset email to the registered user.

    Args:
        to: The email address to send to.

    Return:
    """
    
    token = generate_conformation_token(email=to)
    confirm_url = url_for('auth_reset_password_by_email_confirmation', token=token, _external=True)
    html = render_template('password_reset.html', confirm_url=confirm_url)
    send_email(to, 'Yêu cầu thay đổi mật khẩu', html)


def get_response_message(message):
    """ Get HTML message to return to user.

    Args:
         message: The message to return.

    Return:
    """
    
    html = render_template('response.html', message=message)
    return html


def encode_auth_token(user_id, delta=timedelta(days=30, seconds=5)):
    ''' Generate the Auth token.

    Args:
        user_id: The user's ID to generate token

    Return:
        string
    '''
    
    try:
        payload = {
            'exp': datetime.utcnow() + delta,
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            BaseConfig.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        print(e.__str__())
        return None


def decode_auth_token(auth_token):
    """ Validates the auth token

    Args:
         auth_token:

    Return:
         integer|string
    """

    try:
        payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY)
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return None, 'Token blacklisted. Please log in again.'
        else:
            return payload['sub'], ''  # return the user_id
    except jwt.ExpiredSignatureError:
        return None, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return None, 'Invalid token. Please log in again.'


def password_validator(form, field):
    """Ensure that passwords have at least 6 characters with one lowercase letter, one uppercase letter and one number.
        Override this method to customize the password validator.
    """

    # Convert string to list of characters
    password = list(field.data)
    password_length = len(password)

    # Count lowercase, uppercase and numbers
    lowers = uppers = digits = 0
    for ch in password:
        if ch.islower():
            lowers += 1
        if ch.isupper():
            uppers += 1
        if ch.isdigit():
            digits += 1

    # Password must have one lowercase letter, one uppercase letter and one digit
    is_valid = password_length >= 6 and lowers and uppers and digits
    if not is_valid:
        raise ValidationError(_l(
            'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))


def username_validator(form, field):
    """Ensure that Usernames contains at least 5 alphanumeric characters.
    """

    username = field.data
    if len(username) < 5:
        raise ValidationError(_l('Username must be at least 5 characters long'))
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._'
    chars = list(username)
    for char in chars:
        if char not in valid_chars:
            raise ValidationError(_l("Username may only contain letters, numbers, '-', '.' and '_'"))


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def convert_markdown(string):
    """Convert the argument from markdown to html"""
    return markdown2.markdown(string,
                              extras=["code-friendly", "code-color", "footnotes"])


def remove_markdown(text):
    return __md.convert(text)


def no_accent_vietnamese(s):
    """ Convert accented Vietnamese into unsigned
    """
    
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


def send_verification_sms(to=''):
    """ Send verification code to that phone number
    """
    
    user = User.query.filter_by(phone_number=to).first()
    service = BaseConfig.VERIFICATION_SID
    verification = client.verify \
        .services(service) \
        .verifications \
        .create(to=to, channel='sms')

    if verification and verification.sid and user:
        user.verification_sms_time = datetime.utcnow()
        db.session.commit()
    
    return verification.sid


def is_valid_username(user_name):
    """ Ensure that username only has letter, number and chraters (_.-).
        
    Args:
        user_name (string): display name
    
    Returns:
        Boolean
    """
    
    return re.match("^[a-zA-Z0-9_.-]+$", user_name) is not None


def validate_phone_number(phone_number):
    """ Ensure that is correct phone number.
    """
    
    try:
        phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number)
    except Exception as e:
        logger.error(e.__str__())
        return False
    # return re.match('^(09|01[2|6|8|9])+([0-9]{8})$', phone_number)


def check_verification(phone, code):
    """ Verify code sent to that phone number
    """
    
    user = User.query.filter_by(phone_number=phone).first()
    service = BaseConfig.VERIFICATION_SID
    
    try:
        verification_check = client.verify \
            .services(service) \
            .verification_checks \
            .create(to=phone, code=code)

        if verification_check.status == "approved":
            current_time = datetime.utcnow()
            difference = current_time - user.verification_sms_time
            return difference.seconds <= BaseConfig.LIMIT_VERIFY_SMS_TIME
        return False
    
    except Exception as e:
        return False


def check_password(password):
    """ Ensure that passwords have at least 8 characters with two uppercase letters, two numbers and two special characters.
    """

    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=1,  # need min. 1 uppercase letters
        numbers=1,  # need min. 1 digits
        special=1,  # need min. 1 special characters
        #nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
    )
    return policy.test(password)


def is_valid_email(email):
    """ Validate email address

        Args:
            email (string): email address

        Returns:
            boolean   
    """

    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.search(regex, email) is not None

