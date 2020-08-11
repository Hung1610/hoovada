#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
import hmac
import hashlib
import requests
from datetime import datetime, timedelta

# third-party modules
import chardet
from flask import make_response, request
from flask_restx import marshal

# own modules
from app.settings.config import BaseConfig as Config
from app import db
from app.modules.auth.auth_dto import AuthDto
from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User, SocialAccount
from app.modules.user.user import User
from app.modules.user.user_dto import UserDto
from app.utils.response import send_error, send_result
from app.utils.util import send_confirmation_email, confirm_token, decode_auth_token, encode_auth_token, \
    get_response_message, no_accent_vietnamese, validate_phone_number, is_valid_username, send_verification_sms, \
    check_verification, check_password, is_valid_email, generate_confirmation_token, send_password_reset_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        return send_result(message='Successfully logged out.')
    except Exception as e:
        db.session.rollback()
        return send_error(message=e)


# def generate_confirmation_token(email):
#     """Confirmation email token"""
#     serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
#     return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
#
#
# def confirm_token(token, expiration=3600):
#     """Plausibility check of confirmation token."""
#     serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
#     try:
#         email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration)
#     except:
#         return False
#     return email
#
#
# def send_confirmation_email(to):
#     """Send a confirmation email to the registered user"""
#     token = generate_confirmation_token(email=to)
#     confirm_url = url_for('confirmationview', token=token, _external=True)
#     html = render_template('app/templates/confirmation.html', confirm_url=confirm_url)
#     # send_email(subject='Email confirmation', sender=Config.MAIL_DEFAULT_SENDER, recipients=to, html_body=html)


def get_id(user_id, role):
    pass


def save_social_account(provider, extra_data):
    social_account = SocialAccount.query.filter_by(uid=extra_data.get('id')).first()
    if social_account is not None:
        user = User.query.filter_by(id=social_account.user_id).first()
        if (user is not None):
            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})
        return send_error(message="Đăng nhập thất bại, vui lòng thử lại!")
    else:
        email = extra_data.get('email', '')
        if (AuthController.check_user_exist(email)):
            return send_error(message='Người dùng với địa chỉ Email {} đã tồn tại, vui lòng đăng nhập.'.format(email))
            
        user_name = no_accent_vietnamese(extra_data['name']).strip().replace(' ', '_').lower()
        user_name = AuthController.create_user_name(user_name)
        # display_name = extra_data.get('name', '')
        first_name = extra_data.get('first_name', '')
        last_name = extra_data.get('last_name', '')
        middle_name = extra_data.get('middle_name', '')
        user = User(display_name=user_name, email=email, confirmed=True, first_name=first_name, middle_name=middle_name, last_name=last_name)
        user.set_password(password=provider + '_' + str(user_name))
        
        try:
            db.session.add(user)
            db.session.commit()
            social_account = SocialAccount(provider=provider, uid=extra_data.get('id'), extra_data=json.dumps(extra_data), user_id=user.id)
            db.session.add(social_account)
            db.session.commit()
            auth_token = encode_auth_token(user_id=user.id)
            if auth_token:
                return send_result(data={'access_token': auth_token.decode('utf8')})
            return send_error(message="Đăng nhập thất bại, vui lòng thử lại!")
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return send_error(message="Đăng nhập thất bại, vui lòng thử lại!")


class AuthController:
    """
    This class is used to authenticate and authorize the user.
    """

    @staticmethod
    def check_user_exist(email):
        """ Check user exist by its email. One email on one register
        
        Args:
            email (string)

        Return:
            Boolean
        """

        # password_hash = generate_password_hash(password=password)
        user = User.query.filter_by(email=email).first()
        if user is not None:  # user is exist.
            return True
        else:
            return False


    @staticmethod
    def check_phone_number_exist(phone_number):
        """ Check phone number exist by its phone_number. One phone number on one register
        
        Args:
            phone_number (string)
        
        Returns
            Boolean
        """

        # password_hash = generate_password_hash(password=password)
        user = User.query.filter_by(phone_number=phone_number).first()
        if user is not None:  # user is exist.
            return True
        else:
            return False


    @staticmethod
    def check_user_name_exist(user_name):
        """ Check user exist by its user_name. One user_name on one register
        
        Args:
            user_name (string)
        
        Returns:
            Boolean
        """

        # password_hash = generate_password_hash(password=password)
        user = User.query.filter_by(display_name=user_name).first()
        return user is not None


    @staticmethod
    def create_user_name(user_name):
        """ Create a unique user_name, if it exists in DB we will add "_1", "_2"... until it not exists in DB
        
        Args:
            user_name (string)
        
        Returns
            String
        """
        if (not AuthController.check_user_name_exist(user_name)):
            return user_name
        count = 1
        while AuthController.check_user_name_exist(user_name + '_' + str(count)):
            count += 1
        return user_name + '_' + str(count)


    def login_with_google(self, data):

        if not isinstance(data, dict):
            return send_error( message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')

        if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
            return send_error(message="Vui lòng cung cấp access_token!")
        
        access_token = str(data['access_token'])
        resp = requests.get(Config.GOOGLE_PROFILE_URL, params={'access_token': access_token, 'alt': 'json'})
        
        resp.raise_for_status()
        extra_data = resp.json()
        return save_social_account('google', extra_data)


    def login_with_facebook(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')

        if not 'access_token' in data or str(data['access_token']).strip().__eq__(''):
            return send_error(message="Vui lòng cung cấp access_token!")

        access_token = str(data['access_token'])
        key = Config.FACEBOOK_SECRET.encode('utf-8')
        msg = access_token.encode('utf-8')
        appsecret_proof = hmac.new(key, msg, hashlib.sha256).hexdigest()
        resp = requests.get(
            Config.GRAPH_API_URL,
            params={
                'fields': ','.join(Config.FACEBOOK_FIELDS),
                'access_token': access_token,
                'appsecret_proof': appsecret_proof
            })

        if (resp.status_code != 200):
            return send_error(message="Access token không đúng hoặc hết hạn, vui lòng thử lại!")
        
        resp.raise_for_status()
        extra_data = resp.json()
        return save_social_account('facebook', extra_data)


    def sms_register(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.')
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp số điện thoại!")

        if not 'password' in data or str(data['password']).strip().__eq__(''):
            # Pleases provide a password.')
            return send_error(message='Vui lòng cung cấp mật khẩu')

        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            # Pleases provide a username.')
            return send_error(message='Vui lòng cung cấp username')
        
        if len(check_password(data['password'])) > 0:
            return send_error(message='Mật khẩu phải có ít nhất 8 kí tự,phải có ít nhất 1 kí tự viết hoa, 1 số, 1 kí tự đặc biệt.')
        
        display_name = data['display_name']
        if is_valid_username(display_name) is False:
            return send_error(message='Tên hiển thị chỉ chấp nhận chữ, số và các kí tự "-._"')
        
        if AuthController.check_user_name_exist(display_name):
            return send_error(message='Người dùng với tên {} đã tồn tại, vui lòng thử lại!'.format(display_name))  # User already exist.')

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
        
        if AuthController.check_phone_number_exist(phone_number):
            return send_error(message='Số điện thoại đã tồn tại, vui lòng đăng nhập!')
        # display_name = ''
        password = data['password']
        # if 'display_name' in data:
        #     display_name = data['display_name']
        code = send_verification_sms(phone_number)
        if code is not None:
            user = User(display_name=display_name, phone_number=phone_number, confirmed=False)
            user.set_password(password=password)

            try:
                db.session.add(user)
                db.session.commit()
                return send_result(message='Chúng tôi đã gửi mã kích hoạt đến số điện thoại {}. Vui lòng kiểm tra tin nhắn.'. format(phone_number))
            
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                return send_error(message='Đăng kí thất bại, vui lòng thử lại!')
        else:
           return send_error(message='Số điện thoại không đúng định dạng!')


    def confirm_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng hoặc thiếu, vui lòng kiểm tra lại')
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp số điện thoại!")
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp mã xác nhận!")
        
        code = data['code']
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if user:
            if user.confirmed:
                return send_error(message='Tài khoản của bạn đã được kích hoạt trước đó, vui lòng đăng nhập!')
            else:
                if check_verification(phone_number, code):
                    user.confirmed = True
                    db.session.commit()
                    return send_result(message='Tài khoản của bạn đã được kích hoạt. vui lòng đăng nhập!')
                return send_error(message='Mã không đúng hoặc đã hết hạn. Vui lòng thử lại!')
        else:
            return send_error(message='Số điện thoại {} chưa đăng kí, vui lòng kiểm tra lại!'.format(phone_number))
    

    # @staticmethod
    def resend_confirmation_sms(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')

        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message="Vui lòng cung cấp số điện thoại!")
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
        
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
        """ Login user handling.
        """
    
        try:
            # print(data)
            user = User.query.filter_by(phone_number=data['phone_number']).first()
            if user and user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation_sms(data)
                    return send_error(message='Tài khoản với số điện thoại của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực.')  # Tài khoản email của bạn chưa được xác nhận. Vui lòng đăng nhập hộp thư của bạn để tiến hành xác thực (Trong trường hợp không thấy thư kích hoạt trong hộp thư đến, vui long kiểm tra mục thư rác).')
                
                auth_token = encode_auth_token(user_id=user.id)
                user.active = True
                db.session.commit()
                # if user.blocked:
                #     return None  # error(message='User has been blocked')
                if auth_token:
                    return send_result(data={'access_token': auth_token.decode('utf8')})
                    # return send_result(message=auth_token)  # user
            else:
                return send_error(message='Số điện thoại hoặc mật khẩu không đúng, vui lòng thử lại')  # Email or Password does not match')
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại.')  # Could not login, please try again later. Error {}'.format(e.__str__()))


    def sms_login_with_code(self, data):
        """ Login user handling.
        """

        try:
            # print(data)
            user = User.query.filter_by(phone_number=data['phone_number']).first()
            if user:
                if not user.confirmed:
                    self.resend_confirmation_sms(data)
                    return send_error(message='Tài khoản với số điệnt thoại của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực!')  # Tài khoản email của bạn chưa được xác nhận. Vui lòng đăng nhập hộp thư của bạn để tiến hành xác thực (Trong trường hợp không thấy thư kích hoạt trong hộp thư đến, vui long kiểm tra mục thư rác).')
               
                code = send_verification_sms(data['phone_number'])
                if code is not None:
                    return send_result(message='Chúng tôi đã gửi mã xác nhận tới số điện thoại {}, vui lòng kiểm tra!'.format(
                data['phone_number']))
            else:
                return send_error(message='Số điện thoại không đúng, vui lòng thử lại!')  # Email or Password does not match')
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại!')  # Could not login, please try again later. Error {}'.format(e.__str__()))
    

    def sms_login_with_code_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            return send_error(message="Vui lòng cung cấp số điện thoại!")
        
        phone_number = data['phone_number']
        code = data['code']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp mã xác nhận!")
        
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            if not user.confirmed:
                self.resend_confirmation_sms(data)
                return send_error(message='Tài khoản của bạn chưa được xác nhận. Vui lòng kiểm tra tin nhắn để tiến hành xác thực!')
            
            if check_verification(phone_number, code):
                auth_token = encode_auth_token(user_id=user.id)
                user.active = True
                db.session.commit()
                # if user.blocked:
                #     return None  # error(message='User has been blocked')
                if auth_token:
                    return {'access_token': auth_token.decode('utf8')}
            else:
                return send_error(message='Mã đăng nhập không đúng hoặc đã hết hạn, vui lòng thử lại!')

        return send_error(message='Đăng nhập thất bại, vui lòng thử lại!')


    # @staticmethod
    def register(self, data):
        if not isinstance(data, dict):
            return send_error(
                message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.')
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp Email!')  # Please provide an email")
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')  # Pleases provide a password.')
        
        if not 'display_name' in data or str(data['display_name']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp tên người dùng!') # Pleases provide a username.')

        # check valid email - Vinh
        if is_valid_email(data['email']) is False:
            return send_error(message='Địa chỉ Email không hợp lệ!')
        
        if len(check_password(data['password'])) > 0:
            return send_error(message='Mật khẩu phải có ít nhất 8 kí tự,phải có ít nhất 1 kí tự viết hoa, 1 số, 1 kí tự đặc biệt')
        
        email = data['email']
        display_name = data['display_name']
        password = data['password']
        if AuthController.check_user_exist(email=email):
            return send_error(message='Địa chi email {} đã tồn tại, vui lòng đăng nhập!'.format(email))  # User already exist.')
        
        if AuthController.check_user_name_exist(display_name):
            return send_error(message='Người dùng với tên {} đã tồn tại, vui lòng thử lại!'.format(display_name))  # User already exist.')
        
        user = User(display_name=display_name, email=email, confirmed=False)
        user.set_password(password=password)

        try:
            # user.save()
            db.session.add(user)
            db.session.commit()
            is_confirmed = True  # if saving is successfull --> send confirmation
        except Exception as e:
            print(e.__str__())
            is_confirmed = False
            db.session.rollback()
        if is_confirmed:
            try:
                send_confirmation_email(to=user.email)
                return send_result(message='Chúng tôi đã gửi thư kích hoạt vào hòm thư của bạn. Vui lòng kiểm tra hòm thư!')  # An email has sent to your mailbox. Please check your email to confirm.')
            
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                return send_error(message='Không thể gửi thư kích hoạt vào email của bạn. Vui lòng thử lại!')  # Could not send a confirmation email to your mailbox.')


    def reset_password_by_sms(self, data):
        """Reset password request by SMS OTP
        """        
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.')
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp số điện thoại!")

        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
        
        if not check_phone_number_exist(phone_number):
            return send_error(message='Người dùng chưa tồn tại, vui lòng đăng ký!')

        try:
            code = send_verification_sms(phone_number)
            return send_result(message='Đã gửi OTP đến số điện thoại đăng ký.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư reset password vào email của bạn. Vui lòng thử lại!')

    def reset_password_by_sms_confirm(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng hoặc thiếu, vui lòng kiểm tra lại')
        
        if not 'phone_number' in data or str(data['phone_number']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp số điện thoại!")
        
        if not 'code' in data or str(data['code']).strip().__eq__(''):
            # Please provide an phone_number")
            return send_error(message="Vui lòng cung cấp mã xác nhận!")
        
        phone_number = data['phone_number']
        if not validate_phone_number(phone_number):
            return send_error(message='Số điện thoại không đúng định dạng!')
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
        """Reset password request. Send password reset confirmation link to email.
        """        
        if not isinstance(data, dict):
            return send_error(
                message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.')
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp Email!')  # Please provide an email")

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
        """Reset password confirmation after link on email is clicked

        Args:
            token (string): password reset request token

        Returns:
            string: temporal access token for user to reset password 
        """        
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user:
            message = "Xác thực thành công. Hãy nhập mật khẩu mới."
            return send_result(data={'reset_token':token},message=message)
        else:
            message = 'Mã xác thực reset password của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            return send_error(message=message)  # 'Invalid confirmation token.'

    def change_passwork(self, data):
        """Change password for current user
        """        
        if not isinstance(data, dict):
            return send_error(
                message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')  # Pleases provide a password.
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu xác nhận!')  # Pleases provide password confirmation.
        
        if not 'old_password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')  # Pleases provide the old password.

        password_confirm = data['password_confirm']
        password = data['password']
        old_password = data['old_password']
        
        if password != password_confirm:
            return send_error(message='Mật khẩu xác nhận không đúng. Vui lòng nhập lại!')
            
        if len(check_password(password)) > 0:
            return send_error(message='Mật khẩu phải có ít nhất 8 kí tự,phải có ít nhất 1 kí tự viết hoa, 1 số, 1 kí tự đặc biệt!')

        user, _ = get_logged_user(request)
        if user and user.check_password(old_password):
            user.set_password(password=password)
            try:
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                db.session.rollback()
                message = 'Cập nhật mật khẩu thất bại.'
                return send_error(message=message)  # 'Failed password update.'
            return send_result(message='Cập nhật mật khẩu thành công.')
        else:
            message = 'Mật khẩu cũ không đúng!'
            return send_error(message=message)  # 'Invalid confirmation token.'

    def change_passwork_by_token(self, data):
        """Change password using token received in email
        """        
        if not isinstance(data, dict):
            return send_error(
                message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')  # Data is not correct or not in dictionary form. Try again.

        if not 'reset_token' in data or str(data['reset_token']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp token!')  # Pleases provide a valid token.

        if not 'token_type' in data or str(data['token_type']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp token type!')  # Pleases provide a token type. (email/phone)
        
        if not 'password_confirm' in data or str(data['password_confirm']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu xác nhận!')  # Pleases provide the old password.
        
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp mật khẩu!')  # Pleases provide a password.

        token = data['reset_token']
        password_confirm = data['password_confirm']
        password = data['password']
        token_type = data['token_type']
        
        if password != password_confirm:
            return send_error(message='Mật khẩu xác nhận không đúng. Vui lòng nhập lại!')
            
        if len(check_password(password)) > 0:
            return send_error(message='Mật khẩu phải có ít nhất 8 kí tự,phải có ít nhất 1 kí tự viết hoa, 1 số, 1 kí tự đặc biệt!')

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
                return send_error(message=message)  # 'Failed password update.'
            return send_result(message='Cập nhật mật khẩu thành công.')
        else:
            message = 'Mã xác thực reset password của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            return send_error(message=message)  # 'Invalid confirmation token.'

    # @staticmethod
    def resend_confirmation(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng, vui lòng kiểm tra lại!')
        
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message='Vui lòng cung cấp Email!')
        
        email = data['email']
        if not AuthController.check_user_exist(email=email):
            return send_error(message='Người dùng chưa đăng ký!')
        try:
            send_confirmation_email(to=email)
            return send_result(message='Chúng tôi đã gửi thư kích hoạt vào hòm thư của bạn. Vui lòng kiểm tra hòm thư!')
            
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể gửi thư kích hoạt vào email của bạn. Vui lòng thử lại!')

    # @staticmethod
    def confirm_email(self, token):
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirmed:
                # response = {'message': 'Tài khoản email đã được kích hoạt trước đó, vui lòng đăng nhập.'}
                message = 'Tài khoản của bạn đã được kích hoạt trước đó, vui lòng đăng nhập.'
                return send_result(message=message)  # send_result(data=marshal(response, AuthDto.message_response))
            user.confirmed = True
            # user.active = True
            # user.email_confirmed = True
            user.email_confirmed_at = datetime.now()
            db.session.commit()
            # response = {'message': "Tài khoản email của bạn đã được kích hoạt. Vui lòng đăng nhập."}
            message = 'Tài khoản của bạn đã được kích hoạt trước đó, vui lòng đăng nhập.'
            return send_result(message=message)  # send_result(data=marshal(response, AuthDto.message_response))  # 'Your email has been activated. Please login.'  # send_result(message='Account confirmation was successfully.')
        else:
            # message = 'Mã kích hoạt của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang Web <a href="http://hoovada.com">hoovada.com</a> để yêu cầu mã xác thực mới.'
            message = 'Ma kich hoat của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang hoovada.com để yêu cầu mã xác thực mới.'
            # return_message = get_response_message(message=message)
            return send_result(message=message)  # 'Invalid confirmation token.'

    # @staticmethod
    def login_user(self, data):
        """ Login user handling.
        """
        try:
            # print(data)
            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation(data=data)
                    return send_error( message='Tai khoan email cua ban chua duoc xac nhan. Vui long dang nhap hop thu cua ban de tien hanh xac thuc.')  # Tài khoản email của bạn chưa được xác nhận. Vui lòng đăng nhập hộp thư của bạn để tiến hành xác thực (Trong trường hợp không thấy thư kích hoạt trong hộp thư đến, vui long kiểm tra mục thư rác).')
                
                auth_token = encode_auth_token(user_id=user.id)
                user.active = True
                db.session.commit()
                # if user.blocked:
                #     return None  # error(message='User has been blocked')
                if auth_token:
                    return send_result(data={'access_token': auth_token.decode('utf8')})
                    # return send_result(message=auth_token)  # user
            
            else:
                return send_error(message='Email hoặc mật khẩu không đúng, vui lòng thử lại!')  # Email or Password does not match')
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể đăng nhập, vui lòng thử lại!')  # Could not login, please try again later. Error {}'.format(e.__str__()))

    # @staticmethod
    def logout_user(self, req):
        """
        Logout user handling.
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
            return None
        if api_key is not None:
            auth_token = api_key
        if auth_token:
            # get user information, check user exist
            user_id, _ = decode_auth_token(auth_token=auth_token)
            user = User.query.filter_by(id=user_id).first()
            if user is not None:
                user.active = False
                user.last_seen = datetime.now()
                db.session.commit()
            # save token to backlist.
            save_token(token=auth_token)
            return send_result(message='You are logged out.')
            # return redirect('') # to logout page
        else:
            return send_error(message='Provide a valid auth token')

    def get_user_info(self, req):
        """
        Get user information.

        :param req: The request to handle.

        :return:
        """
        user, message = AuthController.get_logged_user(req=req)
        if user is None:
            return send_error(message=message)
        return send_result(data=marshal(user, UserDto.model_response), message='Success')

    @staticmethod
    def get_logged_user(req):
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
            user = User.query.filter_by(id=user_id).first()
            return user, None
        except Exception as e:
            print(e.__str__())
            return None, message

        # auth_token = new_request.headers.get('Authorization')
        # if auth_token:
        #     auth_token = auth_token.split(' ')[1]
        #     resp = User.decode_auth_token(auth_token)
        #     if not isinstance(resp, str):
        #         user = User.query.filter_by(user_id=resp).first()
        #         return user  # tra lai JSON tương ứng về các roles đang thực hiện và các orders.
        #         # # print(user)
        #         # res = {
        #         #         'user_id': user.user_id,
        #         #         'email': user.email,
        #         #         'role': user.role,
        #         #         'name': user.name
        #         #         }
        #         # return result(data=res)
        #     return None  # error(message=resp)
        # else:
        #     return None  # error(message='Provide a valid auth token')
