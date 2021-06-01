#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
from flask.templating import render_template
import requests
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.user.user_dto import UserDto
from app.settings.config import BaseConfig as Config
from common.models.ban import UserBan
from common.models.blacklist import BlacklistToken
from common.models.user import SocialAccount, User
from common.utils.response import send_error, send_result
from common.utils.util import (check_password, check_verification,
                               confirm_token, convert_vietnamese_diacritics,
                               decode_auth_token, encode_auth_token,
                               generate_confirmation_token,
                               is_valid_email,
                               send_confirmation_email, send_email,
                               send_password_reset_email,
                               send_verification_sms, validate_phone_number,
                               create_random_string)
from common.es import get_model
from common.utils.util import strip_tags

ESUser = get_model("User")

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AuthController:

    ##### EMAIL REGISTRATION #####
    def register(self, data):

        
        if not isinstance(data, dict):
            return send_error(
                message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PASSWORD)
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)
        
        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_DISPLAY_NAME)
        
        if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)

        if len(check_password(data['password'])) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)
        
        email = data['email']
        display_name = data['display_name']
        password = data['password']

        banned = UserBan.query.filter(UserBan.ban_by == email).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)

        if User.get_user_by_email(email=email) is not None:
            return send_error(message=messages.ERR_ACCOUNT_EXISTED)

        if check_user_by_display_name(display_name):
            return send_error(message=messages.ERR_DISPLAY_NAME_EXISTED)
            
        try:
            user = create_user_by_email(data)
            send_confirmation_email(to=user.email, user=user)
            return send_result(message=messages.MSG_EMAIL_SENT)
                
        except Exception as e:
            print(e.__str__())
            db.session.rollback()            
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))


    def confirm_email(self, token):

        email = confirm_token(token)
        if email is None or email.strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)

        if is_valid_email(email) is False:
            return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)

        user = User.get_user_by_email(email=email)
        if user is not None and user.confirmed is True:
            return send_result(message=messages.MSG_REGISTRATION_SUCCESS)

        try:
            user.confirmed = True
            user.email_confirmed_at = datetime.now()
            db.session.commit()
            html = render_template('welcome.html', user=user)
            send_email(user.email, 'Hoovada - Chào mừng bạn tham gia vào cộng đồng!', html)
            return send_result(message=messages.MSG_REGISTRATION_SUCCESS)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))


    def resend_confirmation(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)

        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)

        email = data['email']
        user = User.get_user_by_email(email=email)
        
        if not user:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        # if already activated, do not send confirm email
        if user.confirmed is True:
            return send_result(message=messages.MSG_REGISTRATION_SUCCESS)        
        
        try:
            send_confirmation_email(to=email, user=user)
            return send_result(message=messages.MSG_EMAIL_SENT)
            
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))

    
    ##### CHANGE OR RESET PASSWORD BY MAIL #####

    def reset_password_by_email(self, data):
        """Reset password request. Send password reset confirmation link to email."""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)

        if is_valid_email(data['email']) is False:
            return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)

        email = data['email']
        user = User.get_user_by_email(email)
        if not user:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        try:
            send_password_reset_email(to=email)
            return send_result(message=messages.MSG_EMAIL_SENT)
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED.format(e))


    def reset_password_by_email_confirm(self, token):
        """Reset password confirmation after link on email is clicked"""

        email = confirm_token(token)

        if email is None or email.strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)

        if is_valid_email(email) is False:
            return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)   

        user = User.query.filter_by(email=email).first()
        if not user:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        return send_result(data={'reset_token':token}, message=messages.MSG_PASS_INPUT_PROMPT)


    def change_password(self, data):
        """Change password for current user"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PASSWORD)
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)
        
        if not 'old_password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)

        password_confirm = data['password_confirm']
        password = data['password']
        old_password = data['old_password']
        
        if password != password_confirm:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)
            
        if len(check_password(password)) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        user = g.current_user

        if user.check_password(old_password) is False:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)

        try:
            user.set_password(password=password)
            db.session.commit()
            return send_result(message=messages.MSG_RESET_PASSWORD_SUCCESS)
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED) 

    ### EMAIL/PASS login
    def login_user(self, data):
        
        banned = UserBan.query.filter(UserBan.ban_by == data['email']).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)

        user = User.get_user_by_email(data['email'])
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)   

        if user.check_password(data['password']) is False:
            return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)      

        try:
            if not user.confirmed:
                self.resend_confirmation(data=data)
                return send_error(message=messages.MSG_EMAIL_SENT)
            
            # activate when user re-login
            user.is_deactivated = False
            db.session.commit()

            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_FAILED_LOGIN)


    ##### SOCIAL LOGIN/registration #####

    def login_with_google(self, data):

        try:
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_TOKEN)
            
            access_token = str(data['access_token'])
            resp = requests.get(Config.GOOGLE_PROFILE_URL, params={'access_token': access_token, 'alt': 'json'})
            
            resp.raise_for_status()
            extra_data = resp.json()
            user = save_social_account('google', extra_data)
        
            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_SOCIAL_LOGIN_FAILED.format(e))


    def login_with_facebook(self, data):
        try:
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_TOKEN)

            access_token = str(data['access_token'])
            resp = requests.get(
                Config.GRAPH_API_URL,
                params={
                    'fields': ','.join(Config.FACEBOOK_FIELDS),
                    'access_token': access_token,
                })

            resp.raise_for_status()
            extra_data = resp.json()
            user = save_social_account('facebook', extra_data)
        
            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_SOCIAL_LOGIN_FAILED.format(e))


    ##### SMS registration #####
    def sms_register(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_DISPLAY_NAME)

        display_name = data['display_name']
        if check_user_by_display_name(display_name):
            return send_error(message=messages.ERR_DISPLAY_NAME_EXISTED)

        if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PASSWORD)
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)

        if len(check_password(data['password'])) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        banned = UserBan.query.filter(UserBan.ban_by == phone_number).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)
        
        # Check user by phone
        if User.get_user_by_phone_number(phone_number) is not None:
            return send_error(message=messages.ERR_ACCOUNT_EXISTED)

        try:
            password = data['password']
            user = User(display_name=display_name, phone_number=phone_number, confirmed=False)
            user.set_password(password=password)
            db.session.add(user)

            code = send_verification_sms(phone_number)
            if code is None:
                return send_error(message=messages.ERR_INVALID_NUMBER)

            db.session.commit()
            return send_result(message=messages.MSG_PHONE_SENT)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))

       
    def confirm_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE_CODE)
        
        code = data['code']
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        if user.confirmed is True:
            return send_error(message=messages.MSG_REGISTRATION_SUCCESS)

        try:
            if check_verification(phone_number, code) is False:
                return send_error(message=messages.ERR_CODE_INCORRECT_EXPIRED)

            user.confirmed = True
            db.session.commit()
            html = render_template('welcome.html', user=user)
            send_email(user.email, 'Hoovada - Chào mừng bạn tham gia vào cộng đồng!', html)
            return send_result(message=messages.MSG_REGISTRATION_SUCCESS)
                
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))        
            
    
    def resend_confirmation_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)
        
        try:
            code = send_verification_sms(phone_number)
            if code is not None:
                return send_result(message=messages.MSG_PHONE_SENT)
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_REGISTRATION_FAILED.format(e))

    ##### Phone reset password  #####
    def change_password_by_token(self, data):
        """Change password using token received in email""" 

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'reset_token' in data or str(data['reset_token']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp token!') 

        if not 'token_type' in data or str(data['token_type']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp token type!')
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PASSWORD)

        token = data['reset_token']
        password_confirm = data['password_confirm']
        password = data['password']
        token_type = data['token_type']

        if password != password_confirm:
            return send_error(message=messages.ERR_INVALID_CONFIMED_PASSWORD)
            
        if len(check_password(password)) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        if token_type == 'email':
            email = confirm_token(token)
            user = User.get_user_by_email(email)
        else:
            phone_number = confirm_token(token)
            user = User.get_user_by_phone_number(phone_number)

        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)        

        try:
            user.set_password(password=password)
            db.session.commit()
            return send_result(message=messages.MSG_RESET_PASSWORD_SUCCESS)

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED.format(e))      


    def reset_password_by_sms(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT) 
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)      
        
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        code = send_verification_sms(phone_number)
        if code is not None:
            return send_result(message=messages.MSG_PHONE_SENT)


        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED.format(e))  


    def reset_password_by_sms_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE_CODE)
        
        code = data['code']
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        try:
            if check_verification(phone_number, code) is False:
                return send_error(message=messages.ERR_CODE_INCORRECT_EXPIRED)

            return send_result(data={'reset_token':generate_confirmation_token(phone_number)}, message=messages.MSG_PASS_INPUT_PROMPT)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED.format(e))      

    def send_OTP(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        try:
            code = send_verification_sms(phone_number)
            if code is not None:
                return send_result(message=messages.MSG_PHONE_SENT)

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_RESET_PASSWORD_FAILED.format(e))  

    ##### Phone login #####

    def sms_login_with_password(self, data):
        """ Login user with phone number and password"""

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)
            
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        try:
            if user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation_sms(data)
                    return send_error(message=messages.MSG_PHONE_SENT)
                
                user.is_deactivated = False
                db.session.commit()
                auth_token = encode_auth_token(user_id=user.id)
                if auth_token:
                    return send_result(data={'access_token': auth_token.decode('utf8')})
                    
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_FAILED_LOGIN)


    def sms_login_with_code(self, data):
        """ Send code to login"""

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)

        banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_ACCOUNT)
        
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        if user.confirmed is False:
            self.resend_confirmation_sms(data)
            return send_error(message=messages.MSG_PHONE_SENT) 
         
        try:
            code = send_verification_sms(data['phone_number'])
            if code is not None:
                return send_result(message=messages.MSG_PHONE_SENT)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_FAILED_LOGIN)


    def sms_login_with_code_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)

        phone_number = data['phone_number']
        code = data['code']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PHONE_NO_CODE)
        
        user = User.get_user_by_phone_number(phone_number)
        if user is None:
            return send_error(message=messages.ERR_ACCOUNT_NOT_REGISTERED)

        if not user.confirmed:
            self.resend_confirmation_sms(data)
            return send_error(message=messages.MSG_PHONE_SENT)
        
        try: 
            if check_verification(phone_number, code) is True:
                user.is_deactivated = False
                db.session.commit()
                auth_token = encode_auth_token(user_id=user.id)
                if auth_token:
                    return {'access_token': auth_token.decode('utf8')}
            else:
                return send_error(message=messages.ERR_CODE_INCORRECT_EXPIRED)

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_FAILED_LOGIN)

    ##### Change phone number #####
    def change_phone_number_confirm(self, data):
        """Change phone number for current user"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        phone_number = data.get('phone_number')
        if not phone_number:
            return send_error(message=messages.ERR_INVALID_NUMBER)
        
        code = data.get('code')
        if not code:
            return send_error(message=messages.ERR_NO_PHONE_CODE)

        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_INVALID_NUMBER)
            
        user = g.current_user

        if not check_verification(phone_number, code):
            return send_error(message=messages.ERR_CODE_INCORRECT_EXPIRED)

        try:
            user.phone_number = phone_number
            db.session.commit()
            return send_result(message=messages.MSG_CHANGE_NUMBER_SUCCESS)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CHANGE_NUMBER_FAILED.format(e))

    ##### logout ####
    def logout_user(self, req):

        auth_token = None
        api_key = None
        if 'X-API-KEY' in req.headers:
            api_key = req.headers['X-API-KEY']
        
        if 'Authorization' in req.headers:
            auth_token = req.headers.get('Authorization')
        
        if not auth_token and not api_key:
            return None
        
        if api_key is not None:
            auth_token = api_key

        if auth_token is None:
            return send_error(message=messages.ERR_NO_TOKEN)
        
        try:  
            user_id, _ = decode_auth_token(auth_token=auth_token)
            user = User.get_user_by_id(user_id)
            if user is None:
                return send_error(message=messages.ERR_NOT_LOGIN)

            user.last_seen = datetime.now()
            db.session.commit()

            return send_result(message=messages.MSG_LOGOUT_SUCESS)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_LOGOUT_FAILED.format(str(e)))        
            
    def get_user_info(self, req):
        """Get user information"""

        user = g.current_user
        return send_result(data=marshal(user, UserDto.model_response))


def check_user_by_phone_number(phone_number):
    """ Check phone number exist by its phone_number. One phone number on one register"""

    user = User.query.filter_by(phone_number=phone_number).first()
    if user is not None: 
        return True
    else:
        return False


def check_user_by_display_name(display_name):
    """ Check user exist by its user_name. Return True is existed else return False if not existed"""

    user = User.query.filter_by(display_name=display_name).first()
    return user is not None


def create_unique_display_name(display_name):
    """ Create a unique user_name, if it exists in DB we will add "_1", "_2"... until it not exists in DB"""

    if (not check_user_by_display_name(display_name)):
        return display_name
    
    count = 1
    while check_user_by_display_name(display_name + '_' + str(count)):
        count += 1
    return display_name + '_' + str(count)


def create_user_by_email(data):
    try: 
        #user_name = convert_vietnamese_diacritics(extra_data.get('name')).strip().replace(' ', '_').lower()
        email = data['email']
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        middle_name = data.get('middle_name')
        display_name =  data.get('display_name')
        password = data.get('password', create_random_string(8))
        confirmed = data.get('confirmed', False)

        user = User(display_name=display_name, email=email, confirmed=confirmed, first_name=first_name, middle_name=middle_name, last_name=last_name)
        user.set_password(password=password)
        
        if confirmed is True:
            user.email_confirmed_at = datetime.now()

        db.session.add(user)
        db.session.flush()
        user_dsl = ESUser(_id=user.id, display_name=user.display_name, email=user.email,
                        gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
        user_dsl.save()
        db.session.commit()
        return user

    except Exception as e:
        print(e.__str__())
        db.session.rollback()
        query = db.session.query(User).filter(User.email == data['email'])
        if query is None:
            query.delete()
            db.session.commit()
        raise e


def save_social_account(provider, data):

    if not 'email' in data or str(data['email']).strip().__eq__(''):
        return send_error(message=messages.ERR_NO_MAIL)

    if is_valid_email(data['email']) is False:
        return send_error(message=messages.ERR_INVALID_INPUT_EMAIL)

    email = data['email']
    banned = UserBan.query.filter(UserBan.ban_by == email).first()
    if banned is not None:
        raise Exception(messages.ERR_BANNED_ACCOUNT)

    display_name = data.get('name', email).strip()
    data['display_name'] = create_unique_display_name(display_name)

    try:
        user = User.get_user_by_email(email)
        if not user:
            data['confirmed'] = True
            user = create_user_by_email(data)
        
        if user.confirmed is False:
            user.confirmed = True
            user.email_confirmed_at = datetime.now()
            
        user.is_deactivated = False
        social_account = SocialAccount.query.filter_by(uid=data['id']).first()
        if social_account is None:            
            social_account = SocialAccount(provider=provider, uid=data['id'], extra_data=json.dumps(data), user_id=user.id)
            db.session.add(social_account)

        if social_account.user_id != user.id:
            social_account.user_id = user.id

        db.session.commit()
        return user

    except Exception as e:
        print(e.__str__())
        raise e      
