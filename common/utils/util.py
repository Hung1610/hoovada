#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains some useful and essential function utilities."""

import hashlib
# bulit-in modules
import re
from datetime import datetime, timedelta
from io import StringIO

# third-party modules
import jwt
import markdown2
import phonenumbers
from flask import current_app, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_mail import Message
from flask_restx import ValidationError
from itsdangerous import URLSafeTimedSerializer
from markdown import Markdown
from password_strength import PasswordPolicy
from twilio.rest import Client

# own modules
from common.settings.config import CommonBaseConfig
from common.db import db
from common.mail import mail

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


client = Client(username=CommonBaseConfig.TWILIO_ACCOUNT_SID, password=CommonBaseConfig.TWILIO_AUTH_TOKEN)


def encode_file_name(filename):
    """ Encode the filename (without extension).

    Args:
        filename: The filename.

    Returns:
        string - The encoded filename.
    """

    now = datetime.now()

    encoded = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return '{}{}'.format(now.isoformat(), encoded)


def generate_confirmation_token(email):
    """ Confirmation email token

    Args:
        email: The email used to generate confirmation token.

    Returns:
        string

    """
    serializer = URLSafeTimedSerializer(CommonBaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=CommonBaseConfig.SECURITY_SALT)


def confirm_token(token, expirations=3600):
    """ Confirm token.

    Args:
        token (string): The token to confirm.
        expirations (int): The expiration time.

    Returns:
         email if success and None vice versa.
    """

    serializer = URLSafeTimedSerializer(CommonBaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=CommonBaseConfig.SECURITY_SALT, max_age=expirations)
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
        None
    """
    if to:
        msg = Message(subject, sender=CommonBaseConfig.MAIL_USERNAME, recipients=[to], html=template, charset='utf-8')
        mail.send(msg)


def send_confirmation_email(to, user=None):
    """ Send a confirmation email to the registered user.

    Args:
        to: The email address to send to.

    Returns:
        None
    """
    
    token = generate_confirmation_token(email=to)
    confirm_url = '{}/{}{}'.format(current_app.config['DOMAIN_URL'], '?page=signup_success&token=', token)
    html = render_template('confirmation.html', confirm_url=confirm_url, user=user)
    send_email(to, 'X�c th?c t�i kho?n hoovada.com!', html)


def send_password_reset_email(to):
    """ Send a password reset email to the registered user.

    Args:
        to: The email address to send to.

    Returns:
        None
    """
    
    token = generate_confirmation_token(email=to)
    html = render_template('reset_password.html', token=token)
    send_email(to, 'Hoovada - Thay ??i m?t kh?u!', html)


def send_answer_notif_email(user, answer, question):
    if user and not (user.is_deactivated):
        html = render_template('notif_answer.html', user=user, answer=answer, question=question)
        send_email(user.email, 'B?n nh?n ???c c�u tr? l?i m?i cho c�u h?i c?a b?n t? c?ng ??ng hoovada.com', html)


def send_article_comment_notif_email(user, comment, article):
    if user and not (user.is_deactivated):
        html = render_template('notif_article_comment.html', user=user, comment=comment, article=article)
        send_email(user.email, 'B?n nh?n ???c b�nh lu?n m?i cho b�i vi?t c?a b?n t? c?ng ??ng hoovada.com', html)


def send_question_comment_notif_email(user, comment, question):
    if user and not (user.is_deactivated):
        html = render_template('notif_question_comment.html', user=user, comment=comment, question=question)
        send_email(user.email, 'B?n nh?n ???c b�nh lu?n m?i cho c�u h?i c?a b?n t? c?ng ??ng hoovada.com', html)


def send_answer_comment_notif_email(user, comment, answer):
    if user and not (user.is_deactivated):
        html = render_template('notif_answer_comment.html', user=user, comment=comment, answer=answer)
        send_email(user.email, 'B?n nh?n ???c b�nh lu?n m?i cho c�u tr? l?i c?a b?n t? c?ng ??ng hoovada.com', html)


def send_question_invite_notif_email(user, inviter, question):
    if user and not (user.is_deactivated):
        html = render_template('notif_question_invite.html', inviter=inviter, user=user, question=question)
        send_email(user.email, 'B?n nh?n ???c l?i m?i tr? l?i c�u h?i t? c?ng ??ng hoovada.com', html)


def send_friend_request_notif_email(user, requester):
    if user and not (user.is_deactivated):
        html = render_template('notif_friend_request.html', requester=requester, user=user)
        send_email(user.email, 'B?n nh?n ???c l?i m?i k?t b?n t? c?ng ??ng hoovada.com', html)


def send_follow_request_notif_email(user, requester):
    if user and not (user.is_deactivated):
        html = render_template('notif_follow_request.html', requester=requester, user=user)
        send_email(user.email, 'B?n c� ng??i theo d�i m?i t? c?ng ??ng hoovada.com', html)
    

def send_article_notif_email(user, article):
    if user and not (user.is_deactivated):
        html = render_template('notif_article.html', article=article, user=user)
        send_email(user.email, 'B�i vi?t m?i t? c?ng ??ng hoovada.com', html)
    

def send_question_notif_email(user, question):
    if user and not (user.is_deactivated):
        html = render_template('notif_question.html', question=question, user=user)
        send_email(user.email, 'C�u h?i m?i t? c?ng ??ng hoovada.com', html)


def get_response_message(message):
    """ Get HTML message to return to user.

    Args:
        message: The message to return.

    Returns:
        string
    """
    
    html = render_template('response.html', message=message)
    return html


def encode_auth_token(user_id, delta=timedelta(days=30, seconds=5)):
    """ Generate the Auth token.

    Args:
        user_id (int): The user's ID to generate token

    Returns:
        string
    """
    
    try:
        payload = {
            'exp': datetime.utcnow() + delta,
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            CommonBaseConfig.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        print(e.__str__())
        return None


def decode_auth_token(auth_token):
    """ Validates the auth token

    Args:
        auth_token (string): coded authentication token sent with request

    Returns:
        integer - user_id or None
    """

    try:
        payload = jwt.decode(auth_token, CommonBaseConfig.SECRET_KEY)
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


def convert_vietnamese_diacritics(s):
    """ Convert accented Vietnamese into unsigned

    Args:
        s (string)

    Returns:
        string
    """
    
    s = re.sub(r'[��??��???????????]', 'a', s)
    s = re.sub(r'[��??�??????�?????]', 'A', s)
    s = re.sub(r'[��???�?????]', 'e', s)
    s = re.sub(r'[�???�?????]', 'E', s)
    s = re.sub(r'[��??��???????????]', 'o', s)
    s = re.sub(r'[��??��???????????]', 'O', s)
    s = re.sub(r'[��???]', 'i', s)
    s = re.sub(r'[��???]', 'I', s)
    s = re.sub(r'[��?????????]', 'u', s)
    s = re.sub(r'[??????��???]', 'U', s)
    s = re.sub(r'[?????]', 'y', s)
    s = re.sub(r'[?????]', 'Y', s)
    s = re.sub(r'[?]', 'D', s)
    s = re.sub(r'[?]', 'd', s)
    return s


def send_verification_sms(to=''):
    """ Send verification code to that phone number
    """
    
    user = db.get_model(current_app.config['USER_MODEL_NAME']).query.filter_by(phone_number=to).first()
    service = CommonBaseConfig.VERIFICATION_SID
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
    
    valid_regex = re.match("^[a-zA-Z0-9_.-]+$", user_name) is not None
    valid_name = ~(user_name.lower() == "kh�ch" or user_name.lower() == "?n danh")
    return valid_regex and valid_name


def validate_phone_number(phone_number):
    """Ensure that is correct phone number.
    
    Args:
        phone_number (string)

    Returns:
        Boolean
    """
    
    try:
        phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number)
    except Exception as e:
        print(e.__str__())
        return False
    # return re.match('^(09|01[2|6|8|9])+([0-9]{8})$', phone_number)


def check_verification(phone, code):
    """ Verify code sent to that phone number
    """
    
    user = db.get_model(current_app.config['USER_MODEL_NAME']).query.filter_by(phone_number=phone).first()
    service = CommonBaseConfig.VERIFICATION_SID
    
    try:
        verification_check = client.verify \
            .services(service) \
            .verification_checks \
            .create(to=phone, code=code)

        if verification_check.status == "approved":
            current_time = datetime.utcnow()
            difference = current_time - user.verification_sms_time
            return difference.seconds <= CommonBaseConfig.LIMIT_VERIFY_SMS_TIME
        return False
    
    except Exception as e:
        return False


def check_password(password):
    """ Ensure that passwords have at least 8 characters with two uppercase letters, two numbers and two special characters.
    """

    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        #uppercase=1,  # need min. 1 uppercase letters
        numbers=1,  # need min. 1 digits
        #special=1,  # need min. 1 special characters
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


def get_logged_user(self, req):
    """ User information retrieving.
    """
    auth_token = None
    api_key = None
    # auth = False
    if 'X-API-KEY' in req.headers:
        api_key = req.headers['X-API-KEY']
    if 'Authorization' in req.headers:
        auth_token = req.headers.get('Authorization')
    if not auth_token and not api_key:
        # auth = False
        return None, 'You must provide a valid token to continue.'
    if api_key is not None:
        auth_token = api_key
    user_id, message = decode_auth_token(auth_token=auth_token)
    if user_id is None:
        return None, message
    try:
        user = db.get_model(current_app.config['USER_MODEL_NAME']).query.filter_by(id=user_id).first()
        return user, None
    except Exception as e:
        print(e.__str__())
        return None, message