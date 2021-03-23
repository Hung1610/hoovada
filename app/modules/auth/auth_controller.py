#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
from flask.templating import render_template
import requests
from flask import current_app, request, g
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
                               send_verification_sms, validate_phone_number)

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        return send_result(message=messages.MSG_LOGOUT_SUCESS)
    except Exception as e:
        db.session.rollback()
        return send_error(message=e)

def save_social_account(provider, extra_data):
    social_account = SocialAccount.query.filter_by(uid=extra_data.get('id')).first()
    if social_account:
        user = User.query.filter_by(id=social_account.user_id).first()
        if not user:
            raise Exception(messages.ERR_FAILED_LOGIN)
        return user
        
    email = extra_data.get('email', '')
    
    banned = UserBan.query.filter(UserBan.ban_by == email).first()
    if banned:
        raise Exception(messages.ERR_BANNED_EMAIL)
    
    user = g.current_user
    if not user:
        user = User.query.filter_by(email=email).first()
        if not user:
            #user_name = convert_vietnamese_diacritics(extra_data.get('name')).strip().replace(' ', '_').lower()
            user_name = AuthController.create_user_name(user_name)

            first_name = extra_data.get('first_name', '').strip()
            last_name = extra_data.get('last_name', '').strip()
            middle_name = extra_data.get('middle_name', '').strip()

            if 'name' in  extra_data:
                user_name = extra_data.get('name')
            else:
                user_name = (first_name + " " + middle_name + " " + last_name)

            user_name = user_name.strip()
            user = User(display_name=user_name, email=email, confirmed=True, first_name=first_name, middle_name=middle_name, last_name=last_name)
            user.set_password(password=provider + '_' + str(user_name))
            user.is_deactivated == False
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(e)
                raise e
    
    try:
        social_account = SocialAccount(provider=provider, uid=extra_data.get('id'), extra_data=json.dumps(extra_data), user_id=user.id)
        db.session.add(social_account)
        db.session.commit()
        return user
    except Exception as e:
        print(e)
        raise e


class AuthController:
    """This class is used to authenticate and authorize the user."""

    @staticmethod
    def check_user_exist(email):
        """ Check user exist by its email. One email on one register """

        user = User.query.filter_by(email=email).first()
        return user


    @staticmethod
    def check_phone_number_exist(phone_number):
        """ Check phone number exist by its phone_number. One phone number on one register"""

        user = User.query.filter_by(phone_number=phone_number).first()
        if user is not None: 
            return True
        else:
            return False


    @staticmethod
    def check_user_name_exist(user_name):
        """ Check user exist by its user_name. Return True is existed else return False if not existed"""

        user = User.query.filter_by(display_name=user_name).first()
        return user is not None


    @staticmethod
    def create_user_name(user_name):
        """ Create a unique user_name, if it exists in DB we will add "_1", "_2"... until it not exists in DB"""

        if (not AuthController.check_user_name_exist(user_name)):
            return user_name
        count = 1
        while AuthController.check_user_name_exist(user_name + '_' + str(count)):
            count += 1
        return user_name + '_' + str(count)


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
            return send_error(message=messages.ERR_ISSUE.format(e))


    def login_with_facebook(self, data):
        try:
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_TOKEN)

            access_token = str(data['access_token'])
            # key = current_app.config['FACEBOOK_SECRET'].encode('utf-8')
            # msg = access_token.encode('utf-8')
            # appsecret_proof = hmac.new(key, msg, hashlib.sha256).hexdigest()
            resp = requests.get(
                Config.GRAPH_API_URL,
                params={
                    'fields': ','.join(Config.FACEBOOK_FIELDS),
                    'access_token': access_token,
                    # 'appsecret_proof': appsecret_proof
                })

            resp.raise_for_status()
            extra_data = resp.json()
            user = save_social_account('facebook', extra_data)
            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})
        except Exception as e:
            return send_error(message=messages.ERR_ISSUE.format(e))


    def sms_register(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)

        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PASSWORD)
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)

        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_NAME)
        
        if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_POLICY_STATUS)
        
        if data['password_confirm'] != data['password']:
            return send_error(message=messages.ERR_WRONG_CONFIMED_PASSWORD)
        
        if len(check_password(data['password'])) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)
        
        is_policy_accepted = data['is_policy_accepted']
        if not is_policy_accepted:
            return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

        display_name = data['display_name']
        # 14/03/2021: now allow space 
        #if is_valid_username(display_name) is False:
        #    return send_error(message=messages.ERR_INVALID_INPUT_NAME)
        
        if AuthController.check_user_name_exist(display_name):
            return send_error(message=messages.ERR_NAME_ALREADY_EXISTED.format(display_name))

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)

        banned = UserBan.query.filter(UserBan.ban_by == phone_number).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_EMAIL)
        
        if AuthController.check_phone_number_exist(phone_number):
            return send_error(message=messages.ERR_PHONE_ALREADY_EXISTED)

        password = data['password']
        code = send_verification_sms(phone_number)
        if code is not None:
            user = User(display_name=display_name, phone_number=phone_number, confirmed=False)
            user.set_password(password=password)

            try:
                db.session.add(user)
                db.session.commit()
                return send_result(message=messages.MSG_PHONE_CODE_SENT.format(phone_number))
            
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                return send_error(message=messages.ERR_REGISTRATION_FAILED)
        else:
           return send_error(message=messages.ERR_PHONE_INCORRECT)


    def confirm_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PHONE_NO_CODE)
        
        code = data['code']
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if user:
            if user.confirmed:
                return send_error(message=messages.MSG_ACC_ALREADY_ACTIVATED)

            else:
                if check_verification(phone_number, code):
                    user.confirmed = True
                    db.session.commit()
                    html = render_template('welcome.html', user=user)
                    send_email(user.email, 'Chào mừng bạn tham gia vào cộng đồng hoovada.com', html)
                    return send_result(message=messages.MSG_ACC_ALREADY_ACTIVATED)

                return send_error(message='Mã không đúng hoặc đã hết hạn. Vui lòng thử lại!')
        else:
            return send_error(message='Số điện thoại {} chưa đăng kí, vui lòng kiểm tra lại!'.format(phone_number))
    

    # @staticmethod
    def resend_confirmation_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)
        
        if not AuthController.check_phone_number_exist(phone_number=phone_number):
            return send_error(message='Người dùng chưa đăng kí!')
        try:
            code = send_verification_sms(phone_number)
            if code is not None:
                return send_result(
                    message='Chúng tôi đã gửi mã kích hoạt đến số điện thoại {}. Vui lòng kiểm tra tin nhắn!'. format(phone_number))
            else:
                return send_error(message='Gửi tin nhắn thất bại, vui lòng thử lại!')

        except Exception as e:
            print(e.__str__())
            return send_error(message='Gửi tin nhắn thất bại, vui lòng thử lại!')
    

    def sms_login_with_password(self, data):
        """ Login user with phone number and password"""
    
        try:
            banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
            if banned:
                raise send_error(message=messages.ERR_BANNED_EMAIL)
            user = User.query.filter_by(phone_number=data['phone_number']).first()
            if user and user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation_sms(data)
                    return send_error(message='Tài khoản với số điện thoại của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực.')
                
                user.is_deactivated = False
                user.active = True
                db.session.commit()

                auth_token = encode_auth_token(user_id=user.id)
                if auth_token:
                    return send_result(data={'access_token': auth_token.decode('utf8')})
                    
            else:
                return send_error(message='Số điện thoại hoặc mật khẩu không đúng, vui lòng thử lại')  # Email or Password does not match')
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại.')


    def sms_login_with_code(self, data):
        """ Login user with phone number and send code """

        try:
            banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
            if banned:
                raise send_error(message=messages.ERR_BANNED_EMAIL)
            user = User.query.filter_by(phone_number=data['phone_number']).first()
            if user:
                if not user.confirmed:
                    self.resend_confirmation_sms(data)
                    return send_error(message='Tài khoản với số điệnt thoại của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực!') 
                
                code = send_verification_sms(data['phone_number'])
                if code is not None:
                    return send_result(message='Chúng tôi đã gửi mã xác nhận tới số điện thoại {}, vui lòng kiểm tra!'.format(data['phone_number']))
            else:
                return send_error(message='Số điện thoại không đúng, vui lòng thử lại!') 
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại!')
    

    def sms_login_with_code_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)
        
        banned = UserBan.query.filter(UserBan.ban_by == data['phone_number']).first()
        if banned:
            raise send_error(message=messages.ERR_BANNED_EMAIL)
        phone_number = data['phone_number']
        code = data['code']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PHONE_NO_CODE)
        
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            if not user.confirmed:
                self.resend_confirmation_sms(data)
                return send_error(message='Tài khoản của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực!')
            
            if check_verification(phone_number, code):
                user.active = True
                user.is_deactivated = False
                db.session.commit()
                auth_token = encode_auth_token(user_id=user.id)
                if auth_token:
                    return {'access_token': auth_token.decode('utf8')}
            else:
                return send_error(message='Mã đăng nhập không đúng hoặc đã hết hạn, vui lòng thử lại!')

        return send_error(message='Đăng nhập thất bại, vui lòng thử lại!')

    def create_user(self, user, password):
        """
        Create new user
        Args:
            user: user object instant
            password: user's password

        Returns: True if create successfully else return error

        """
        try:
            user.set_password(password=password)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            e.__setattr__("is_rollback", True)
            return e

    def delete_user(self, email):
        """
        Delete user
        Args:
            email: email of user
        Returns:

        """
        try:
            query = db.session.query(User).filter(User.email == email)
            query.delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    # @staticmethod
    def register(self, data):
        try:
            if not isinstance(data, dict):
                return send_error(
                    message=messages.ERR_WRONG_DATA_FORMAT)
            
            if not 'email' in data or str(data['email']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_MAIL)
            
            if not 'password' in data or str(data['password']).strip().__eq__(''):
                return send_error(message='Password is missing!')
            
            if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)
            
            if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
                return send_error(message='Display_name is missing!')
            
            if not 'is_policy_accepted' in data or str(data['is_policy_accepted']).strip().__eq__(''):
                return send_error(message=messages.ERR_NO_POLICY_STATUS)

            if is_valid_email(data['email']) is False:
                return send_error(message='Password is not valid!')
            
            if data['password_confirm'] != data['password']:
                return send_error(message='Password confirmation failed!')

            if len(check_password(data['password'])) > 0:
                return send_error(message='Password length must be least 8 with at least 1 number digit!')
            
            email = data['email']
            display_name = data['display_name']
            password = data['password']
            is_policy_accepted = data['is_policy_accepted']

            banned = UserBan.query.filter(UserBan.ban_by == email).first()
            if banned:
                raise send_error(message=messages.ERR_BANNED_EMAIL)

            if not is_policy_accepted:
                return send_error(message=messages.ERR_NO_POLICY_ACCEPTED)

            if AuthController.check_user_exist(email=email):
                return send_error(message='Địa chi email {} đã tồn tại, vui lòng đăng nhập!'.format(email))

            if AuthController.check_user_name_exist(display_name):
                return send_error(message=messages.ERR_NAME_ALREADY_EXISTED.format(display_name))
            
            # 14/03/2021: now allow space   
            #if is_valid_username(display_name) is False:
            #    return send_error(message=messages.ERR_INVALID_INPUT_NAME)
            
            user = User(display_name=display_name, email=email, confirmed=False)
            create_result = self.create_user(user=user, password=password)
            if create_result is True:
                send_confirmation_email(to=user.email, user=user)
                return send_result(message='Chúng tôi đã gửi thư kích hoạt vào hòm thư của bạn. Vui lòng kiểm tra hòm thư!')
            else:
                raise Exception(create_result)
                
        except Exception as e:
            print(e.__str__())
            # if has error and data did not rollback then manual delete user
            if not hasattr(e, 'is_rollback'):
                self.delete_user(data.get('email'))
            return send_error(message='Đăng ký thất bại!')

    def reset_password_by_sms(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT) 
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)
        
        if not AuthController.check_phone_number_exist(phone_number):
            return send_error(message='Người dùng chưa tồn tại, vui lòng đăng ký!')

        try:
            code = send_verification_sms(phone_number)
            return send_result(message='Đã gửi OTP đến số điện thoại đăng ký.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư reset password vào email của bạn. Vui lòng thử lại!')

    def reset_password_by_sms_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_PHONE)
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            return send_error(message=messages.ERR_PHONE_NO_CODE)
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)
        code = data['code']
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if user:
            if check_verification(phone_number, code):
                message = "Xác thực thành công. Hãy nhập mật khẩu mới."
                return send_result(data={'reset_token':generate_confirmation_token(phone_number)},message=message)
            return send_error(message='Mã không đúng hoặc đã hết hạn. Vui lòng thử lại!')
        else:
            return send_error(message='Số điện thoại {} chưa đăng kí, vui lòng kiểm tra lại!'.format(phone_number))

    def reset_password_by_email(self, data):
        """Reset password request. Send password reset confirmation link to email."""

        if not isinstance(data, dict):
            return send_error(
                message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)

        email = data['email']
        if not AuthController.check_user_exist(email):
            return send_error(message='Người dùng chưa đăng ký!')
        try:
            send_password_reset_email(to=email)
            return send_result(message='Đã gửi email reset password đến địa chỉ email đăng ký.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư reset password vào email của bạn. Vui lòng thử lại!')
        
    def reset_password_by_email_confirm(self, token):
        """Reset password confirmation after link on email is clicked"""

        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user:
            message = "Xác thực thành công. Hãy nhập mật khẩu mới."
            return send_result(data={'reset_token':token},message=message)
        else:
            message = 'Mã xác thực reset password của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            return send_error(message=message) 

    def change_password(self, data):
        """Change password for current user"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_CONFIRMED_PASSWORD)
        
        if not 'old_password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')

        password_confirm = data['password_confirm']
        password = data['password']
        old_password = data['old_password']
        
        if password != password_confirm:
            return send_error(message=messages.ERR_WRONG_CONFIMED_PASSWORD)
            
        if len(check_password(password)) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        user, _ = current_app.get_logged_user(request)
        if user and user.check_password(old_password):
            user.set_password(password=password)
            try:
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                message = 'Cập nhật mật khẩu thất bại.'
                return send_error(message=message) 
            return send_result(message='Cập nhật mật khẩu thành công.')
        else:
            message = 'Mật khẩu cũ không đúng!'
            return send_error(message=message)

    def send_OTP(self, data):
        """Reset password request by SMS OTP"""

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        phone_number = data.get('phone_number')
        if not phone_number:
            return send_error(message='Please provide phone number!')

        if not validate_phone_number(phone_number):
            return send_error(message=messages.ERR_PHONE_INCORRECT)

        try:
            code = send_verification_sms(phone_number)
            return send_result(message='Đã gửi OTP đến số điện thoại đăng ký.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư reset password vào email của bạn. Vui lòng thử lại!')

    def change_phone_number_confirm(self, data):
        """Change phone number for current user"""

        try:
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
            
            phone_number = data.get('phone_number')
            if not phone_number:
                return send_error(message='Please provide phone number!')
            
            code = data.get('code')
            if not code:
                return send_error(message='Please provide OTP!')
            if not validate_phone_number(phone_number):
                return send_error(message=messages.ERR_PHONE_INCORRECT)
                
            current_user, _ = current_app.get_logged_user(request)
            
            if current_user:
                if not check_verification(phone_number, code):
                    return send_error(message='Mã không đúng hoặc đã hết hạn. Vui lòng thử lại!')
                current_user.phone_number = phone_number
                db.session.commit()
                return send_result(message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_ISSUE.format(e))

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
            return send_error(message='Vui lòng cung cấp mật khẩu!') 

        token = data['reset_token']
        password_confirm = data['password_confirm']
        password = data['password']
        token_type = data['token_type']
        
        if password != password_confirm:
            return send_error(message=messages.ERR_WRONG_CONFIMED_PASSWORD)
            
        if len(check_password(password)) > 0:
            return send_error(message=messages.ERR_INVALID_INPUT_PASSWORD)

        if token_type == 'email':
            email = confirm_token(token)
            user = User.query.filter_by(email=email).first()
        else:
            phone_number = confirm_token(token)
            user = User.query.filter_by(phone_number=phone_number).first()

        if user :
            user.set_password(password=password)
            try:
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                message = 'Cập nhật mật khẩu thất bại.'
                return send_error(message=message)
            return send_result(message='Cập nhật mật khẩu thành công.')
        else:
            message = 'Mã xác thực reset password của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            return send_error(message=message)

    def resend_confirmation(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message=messages.ERR_NO_MAIL)
        
        email = data['email']
        user = AuthController.check_user_exist(email=email)
        if not user:
            return send_error(message='Người dùng chưa đăng ký!')
        try:
            send_confirmation_email(to=email, user=user)
            return send_result(message='Chúng tôi đã gửi thư kích hoạt vào hòm thư của bạn. Vui lòng kiểm tra hòm thư!')
            
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư kích hoạt vào email của bạn. Vui lòng thử lại!')

    def confirm_email(self, token):
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirmed:
                message = 'Tài khoản của bạn đã được kích hoạt trước đó, vui lòng đăng nhập.'
                return send_result(message=message)

            user.confirmed = True
            user.email_confirmed_at = datetime.now()
            db.session.commit()
            html = render_template('welcome.html', user=user)
            send_email(user.email, 'Chào mừng bạn tham gia vào cộng đồng hoovada.com', html)
            return send_result(message=messages.MSG_ACC_ALREADY_ACTIVATED)
        
        else:
            message = 'Mã kich hoat của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            return send_result(message=message) 

    def login_user(self, data):
        try:
            banned = UserBan.query.filter(UserBan.ban_by == data['email']).first()
            if banned:
                raise send_error(message=messages.ERR_BANNED_EMAIL)

            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation(data=data)
                    return send_error( message=messages.ERR_EMAIL_NOT_CONFIRMED)
                
                # activate when user re-login
                if user.is_deactivated is True:
                    user.is_deactivated = False
                    db.session.commit()

                auth_token = encode_auth_token(user_id=user.id)

                if auth_token:
                    return send_result(data={'access_token': auth_token.decode('utf8')})

            else:
                return send_error(message=messages.ERR_INCORRECT_EMAIL_OR_PASSWORD)
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại!')

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
        if auth_token:
            user_id, _ = decode_auth_token(auth_token=auth_token)
            user = User.query.filter_by(id=user_id).first()
            if user is not None:
                user.active = False
                user.last_seen = datetime.now()
                db.session.commit()
            return send_result(message='You are logged out.')
        else:
            return send_error(message='Provide a valid auth token')

    def get_user_info(self, req):
        """Get user information"""

        user = g.current_user
        if user is None:
            return send_error(message='You are not logged in.')
        return send_result(data=marshal(user, UserDto.model_response), message='Success')
