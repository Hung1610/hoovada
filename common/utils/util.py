#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains some useful and essential function utilities."""

# bulit-in modules
import hashlib
import re
from datetime import datetime, timedelta
from io import StringIO
from html.parser import HTMLParser


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
    now = datetime.now()
    encoded = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return '{}{}'.format(now.isoformat(), encoded)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(CommonBaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=CommonBaseConfig.SECURITY_SALT)


def confirm_token(token, expirations=3600):
    serializer = URLSafeTimedSerializer(CommonBaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=CommonBaseConfig.SECURITY_SALT, max_age=expirations)
        return email
    except Exception as e:
        print(e.__str__())
        return None

def send_email(to, subject, template, sender=(CommonBaseConfig.MAIL_USERNAME, CommonBaseConfig.MAIL_DEFAULT_SENDER)):
    if to:
        msg = Message(subject, sender=sender, recipients=[to], html=template, charset='utf-8')
        mail.send(msg)

def send_confirmation_email(to, user=None):    
    token = generate_confirmation_token(email=to)
    confirm_url = '{}/?page=signup_success&token={}&email={}'.format(current_app.config['DOMAIN_URL'], token, to)
    html = render_template('confirmation.html', confirm_url=confirm_url, user=user)
    send_email(to, 'Hoovada- Xác thực tài khoản!', html, sender=(CommonBaseConfig.AUTHENTICATION_MAIL_USERNAME, CommonBaseConfig.AUTHENTICATION_MAIL_SENDER))

def send_password_reset_email(to):    
    token = generate_confirmation_token(email=to)
    html = render_template('reset_password.html', token=token)
    send_email(to, 'Hoovada - Thay đổi mật khẩu!', html, sender=(CommonBaseConfig.AUTHENTICATION_MAIL_USERNAME, CommonBaseConfig.AUTHENTICATION_MAIL_SENDER))

def send_friend_request_notif_email(user, requester):
    if user and not (user.is_deactivated):
        html = render_template('notif_friend_request.html', requester=requester, user=user)
        send_email(user.email, 'Bạn nhận được lời mời kết bạn từ cộng đồng Hoovada.com', html, sender=(CommonBaseConfig.NOTIFICATION_MAIL_USERNAME, CommonBaseConfig.NOTIFICATION_MAIL_SENDER))

def get_response_message(message):    
    html = render_template('response.html', message=message)
    return html


def encode_auth_token(user_id, delta=timedelta(days=30, seconds=5)):    
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
    try:
        payload = jwt.decode(auth_token, CommonBaseConfig.SECRET_KEY)
        return payload['sub'], ''  # return the user_id
    except jwt.ExpiredSignatureError:
        return None, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return None, 'Invalid token. Please log in again.'

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
    return markdown2.markdown(string,
                              extras=["code-friendly", "code-color", "footnotes"])


def remove_markdown(text):
    return __md.convert(text)


def convert_vietnamese_diacritics(s):
    """ Convert accented Vietnamese into unsigned"""
    
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
    try: 
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
    except Exception as e:
        print(e.__str__())
        db.session.rollback()
        raise e


def is_valid_username(user_name):
    """Verify that user name only has letter, number and chraters (_.-)."""
    
    valid_regex = re.match("^[a-zA-Z0-9_.-]+$", user_name) is not None
    valid_name = ~(user_name.lower() == "khách" or user_name.lower() == "ẩn danh")
    return valid_regex and valid_name


def validate_phone_number(phone_number):
    """Verify valid phone number"""
    
    try:
        phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(phone_number)
    except Exception as e:
        print(e.__str__())
        return False
    # return re.match('^(09|01[2|6|8|9])+([0-9]{8})$', phone_number)


def check_verification(phone, code):
    """ Verify code sent to that phone number"""
    
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
        print(e.__str__())
        return False


def check_password(password):
    """ Verify that passwords have at least 8 characters"""

    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        #uppercase=1,  # need min. 1 uppercase letters
        #numbers=1,  # need min. 1 digits
        #special=1,  # need min. 1 special characters
        #nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
    )
    return policy.test(password)


def is_valid_email(email):
    """ Validate email address"""

    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.search(regex, email) is not None


def get_logged_user(self, req):
    """ User information retrieving."""

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


def create_random_string(length):
    from string import ascii_letters, digits
    from random import choices
    random_string = ''.join(choices(ascii_letters + digits, k = length))
    return random_string

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()