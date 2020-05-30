# -*- coding: utf-8 -*-

"""
File: util.py
Purpose: This file contains some useful and essential function utilities.

This is the applications utilities.
"""
import hashlib
from datetime import datetime, timedelta
from io import StringIO

import jwt
import markdown2
from flask import url_for, render_template
from flask_babel import lazy_gettext as _l
from flask_mail import Message
from flask_restx import ValidationError
from itsdangerous import URLSafeTimedSerializer
from markdown import Markdown

from app.app import mail
from app.modules.user.blacklist import BlacklistToken
from app.settings import config

def encode_file_name(filename):
    '''
    Encode the filename (without extension).

    :param filename: The filename.

    :return: The encoded filename.
    '''
    encoded = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return encoded

def generate_conformation_token(email):
    """
    Confirmation email token

    :param email: The email used to generate confirmation token.

    :return:
    """
    serializer = URLSafeTimedSerializer(config.Config.SECRET_KEY)
    return serializer.dumps(email, salt=config.Config.SECURITY_SALT)


def confirm_token(token, expirations=3600):
    """
    Confirm token.

    :param token: The token to confirm.

    :param expirations: The expiration time.

    :return: email if success and None vice versa.
    """
    serializer = URLSafeTimedSerializer(config.Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=config.Config.SECURITY_SALT, max_age=expirations)
        return email
    except Exception as e:
        print(e.__str__())
        return None


def send_email(to, subject, template):
    """
    Send an email.

    :param to: The email-address to send to.

    :param subject: The subject of the email.

    :param template: The template to generate email.

    :return:
    """
    msg = Message(subject, sender=config.Config.MAIL_USERNAME, recipients=[to], html=template)
    mail.send(msg)


def send_confirmation_email(to):
    """
    Send a confirmation email to the registered user.

    :param to: The email address to send to.

    :return:
    """
    token = generate_conformation_token(email=to)
    confirm_url = url_for('auth_confirmation_email', token=token, _external=True)
    html = render_template('confirmation.html', confirm_url=confirm_url)
    send_email(to, 'Confirmation your registration', html)


def encode_auth_token(user_id):
    '''
    Generate the Auth token.

    :param user_id: The user's ID to generate token

    :return:
    '''
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            config.Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        print(e.__str__())
        return None


def decode_auth_token(auth_token):
    """
    Validates the auth token

    :param auth_token:

    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, config.Config.SECRET_KEY)
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
