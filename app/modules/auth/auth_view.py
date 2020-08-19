#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request

# own modules
from app.modules.auth.auth_controller import AuthController
from app.modules.auth.auth_dto import AuthDto
from app.modules.auth.decorator import token_required
from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AuthDto.api
_auth_register = AuthDto.model_register
_auth_login = AuthDto.model_login
_user_info = UserDto.model_response
_auth_sms_register = AuthDto.model_sms_register
_auth_confirm_sms = AuthDto.model_confirm_sms
_auth_resend_confirm_sms = AuthDto.model_resend_confirmation_sms
_auth_sms_login_with_password = AuthDto.model_sms_login_with_password
_auth_model_sms_login_with_code = AuthDto.model_sms_login_with_code
_auth_model_sms_login_with_code_confirm = AuthDto.model_sms_login_with_code_confirm
_auth_social_login = AuthDto.model_social_login
_auth_reset_password_email = AuthDto.model_reset_password_email
_auth_reset_password_phone = AuthDto.model_reset_password_phone
_auth_change_password_token = AuthDto.model_change_password_token
_auth_change_password = AuthDto.model_change_password


@api.route('/sms/register')
class SmsRegister(Resource):

    @api.expect(_auth_sms_register)
    def post(self):
        """ 
        Register new user with mobile.
        """
        post_data = request.json
        controller = AuthController()
        return controller.sms_register(post_data)


@api.route('/sms/confirm')
class SmsConfirm(Resource):

    @api.expect(_auth_confirm_sms)
    def post(self):
        """ 
        Check confirmation sms code.
        """

        post_data = request.json
        controller = AuthController()
        return controller.confirm_sms(post_data)


@api.route('/sms/resend_confirm')
class SmsResendConfirm(Resource):

    @api.expect(_auth_resend_confirm_sms)
    def post(self):
        """ 
        Resend confirmation sms code.
        """

        post_data = request.json
        controller = AuthController()
        return controller.resend_confirmation_sms(post_data)


@api.route('/sms/login_password')
class SmsLoginPassword(Resource):

    @api.expect(_auth_sms_login_with_password)
    def post(self):
        """ 
        Login with phone number and password.
        """

        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_password(post_data)


@api.route('/sms/login_code')
class SmsLoginCode(Resource):


    @api.expect(_auth_model_sms_login_with_code)
    def post(self):
        """ 
        Login with phone number - the system will send code to user
        """
        
        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_code(post_data)


@api.route('/sms/login_code/confirm')
class SmsLoginCodeConfirm(Resource):

    @api.expect(_auth_model_sms_login_with_code_confirm)
    def post(self):
        """ 
        Confirm sms code that send to user phone number for login
        """

        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_code_confirm(post_data)


@api.route('/register')
class Register(Resource):

    @api.expect(_auth_register)
    def post(self):
        """ 
        Register new user with email and password
        """

        post_data = request.json
        controller = AuthController()
        return controller.register(post_data)


@api.route('/resend_confirmation')
class ResendConfirmation(Resource):

    @api.expect(_auth_login)
    def post(self):
        """ 
        Resend confirmation email
        """

        data = api.payload
        controller = AuthController()
        return controller.resend_confirmation(data=data)


@api.route('/confirmation/<token>')
class ConfirmationEmail(Resource):

    @api.doc(params={'token': 'The token to confirm'})
    def get(self, token):
        """ 
        Check confirmation token sent to email for registration
        """

        controller = AuthController()
        return controller.confirm_email(token=token)


@api.route('/password-reset-email', endpoint='password_reset_email')
class PasswordResetEmail(Resource):

    @api.expect(_auth_reset_password_email)
    def post(self):
        """ 
        Request password reset with email
        """
        post_data = request.json
        controller = AuthController()
        return controller.reset_password_by_email(data=post_data)


@api.route('/password-reset-email-confirm/<token>', endpoint='password_reset_email_confirm')
class PasswordResetEmailConfirm(Resource):
    
    @api.doc(params={'token': 'The token used for confirmation'})
    def post(self, token):
        """ 
        Check confirmation token for password reset with email
        """
        controller = AuthController()
        return controller.reset_password_by_email_confirm(token=token)


@api.route('/password-reset-phone')
class PasswordResetPhone(Resource):

    @api.expect(_auth_reset_password_phone)
    def post(self):
        """ 
        Request password reset with phone number
        """
        post_data = request.json
        controller = AuthController()
        return controller.reset_password_by_sms(data=post_data)


@api.route('/password-reset-phone-confirm/<token>')
class PasswordResetPhoneConfirm(Resource):


    @api.doc(params={'token': 'The token used for confirmation'})
    def post(self, token):
        """ 
        Check token for password reset with phone number.
        """
        post_data = request.json
        controller = AuthController()
        return controller.reset_password_by_sms_confirm(data=post_data)

        
@api.route('/change-password-token')
class ChangePasswordByToken(Resource):

    @api.expect(_auth_change_password_token)
    def post(self):
        """ 
        Change password with reset token
        """
        
        post_data = request.json
        controller = AuthController()
        return controller.change_password_by_token(data=post_data)


@api.route('/change-password')
class ChangePassword(Resource):

    @api.expect(_auth_change_password)
    def post(self):
        """ 
        Allow user to change password
        """
        post_data = request.json
        controller = AuthController()
        return controller.change_password(data=post_data)


@api.route('/login')
class Login(Resource):

    @api.expect(_auth_login)
    def post(self):
        """
        Login user to the system with email and password
        """

        post_data = request.json
        controller = AuthController()
        return controller.login_user(data=post_data)


@api.route('/social_login/facebook')
class FacebookLogin(Resource):

    @api.expect(_auth_social_login)
    def post(self):
        """
        Login user to the system with FB
        """

        post_data = request.json
        controller = AuthController()
        return controller.login_with_facebook(data=post_data)


@api.route('/social_login/google')
class GoogleLogin(Resource):

    @api.expect(_auth_social_login)
    def post(self):
        """ 
        Login user to the system with Google
        """

        post_data = request.json
        controller = AuthController()
        return controller.login_with_google(data=post_data)


@api.route('/logout')
class Logout(Resource):

    @token_required
    def get(self):
        """ 
        Logout the user from the system.
        """

        # auth_header = request.headers.get('Authorization')
        # return ControllerAuth.logout_user(data=auth_header)
        # post_data = request.json
        controller = AuthController()
        return controller.logout_user(req=request)


@api.route('/info')
class UserInfor(Resource):

    @token_required
    @api.response(code=200, model=_user_info, description='Model for user information.')
    def get(self):
        """ 
        Get information from user token
        """

        controller = AuthController()
        return controller.get_user_info(request)
        # return AuthController.get_logged_user(request)
