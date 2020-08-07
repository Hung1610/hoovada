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

@api.route('/sms/register')
class Register(Resource):
    '''
    Register new user with sms
    '''

    @api.expect(_auth_sms_register)
    def post(self):
        ''' Register new user.
        
        Args:
            display_name (string): The name to display in website (optional).
            phone_number (string): The phone_number to register.
            password(string): The password to register.
        
        Returns:
            None, An verification code will be sent to user's phone number to activate account.
        '''
        post_data = request.json
        controller = AuthController()
        return controller.sms_register(post_data)

@api.route('/sms/confirm')
class Register(Resource):
    '''
    Confirm new user registered with sms
    '''

    @api.expect(_auth_confirm_sms)
    def post(self):
        ''' Check confirmation sms code.

        Args:
            phone_number (string): The phone_number to register.

        Returns:
            None, verification code will be sent to user
        '''

        post_data = request.json
        controller = AuthController()
        return controller.confirm_sms(post_data)


@api.route('/sms/resend_confirm')
class Register(Resource):
    '''
    Resend Confirm code to user registered with sms
    '''

    @api.expect(_auth_resend_confirm_sms)
    def post(self):
        ''' Resend confirmation sms code.

        Args:
            phone_number (string): The phone_number to register.

        Returns:
            None, confirmation sms sent to user
        '''

        post_data = request.json
        controller = AuthController()
        return controller.resend_confirmation_sms(post_data)


@api.route('/sms/login_password')
class Register(Resource):
    '''
    API sms login
    '''

    @api.expect(_auth_sms_login_with_password)
    def post(self):
        ''' Login with sms and password.
        
        Args:
            phone_number (string): The phone_number to register.
            password (string): The password to register.

        Returns: 
            None
        '''

        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_password(post_data)


@api.route('/sms/login_code')
class Register(Resource):
    '''
    API sms login
    '''

    @api.expect(_auth_model_sms_login_with_code)
    def post(self):
        ''' Login with sms and password.
        
        Args:
            phone_number (string): The phone_number to register.

        Returns: 
            None
        '''
        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_code(post_data)


@api.route('/sms/login_code/confirm')
class Register(Resource):
    '''
    API sms login
    '''

    @api.expect(_auth_model_sms_login_with_code_confirm)
    def post(self):
        ''' Login with sms and password.
    
        Args:
            phone_number (string): The phone_number to register.
            code (string): The code get from sms.

        Returns:
            None
        '''

        post_data = request.json
        controller = AuthController()
        return controller.sms_login_with_code_confirm(post_data)


@api.route('/register')
class Register(Resource):
    '''
    Register new user with email and password
    '''

    @api.expect(_auth_register)
    def post(self):
        ''' Register new user.
        
        Args:
            display_name: The name to display in website (optional).
            email: The email to register.
            password: The password to register.
        
        Returns:
            None, an confirmation email will be sent to user's mailbox to activate account.
        '''

        post_data = request.json
        controller = AuthController()
        return controller.register(post_data)


@api.route('/resend_confirmation')
class ResendConfirmation(Resource):
    
    @api.expect(_auth_login)
    def post(self):
        ''' Resend confirmation email.
        
        Args:
            None

        Return:
            None
        '''

        data = api.payload
        controller = AuthController()
        return controller.resend_confirmation(data=data)


@api.route('/confirmation/<token>')
class ConfirmationEmail(Resource):

    def get(self, token):
        ''' Check confirmation token.
        
        Args:
            token (string): The token to confirm.

        Returns:
            None
        '''

        controller = AuthController()
        return controller.confirm_email(token=token)


@api.route('/login')
class Login(Resource):
    '''
    API login
    '''

    # @api.expect(_auth)
    @api.expect(_auth_login)
    def post(self):
        """Login user to the system.
        
        Args:
            email (string): the email of the user.
            password (string): the password of the user.

        Returns:
            None, All information of user if he logged in and None if he did not log in.
        """
        post_data = request.json
        controller = AuthController()
        return controller.login_user(data=post_data)


@api.route('/social_login/facebook')
class Login(Resource):
    '''
    API login
    '''

    # @api.expect(_auth)
    @api.expect(_auth_social_login)
    def post(self):
        """ Login user to the system.
        
        Args:
            access_token (string): the access_token get from login facebook on client.

        Returns:   
            All information of user if he logged in and None if he did not log in.
        """
        post_data = request.json
        controller = AuthController()
        return controller.login_with_facebook(data=post_data)


@api.route('/social_login/google')
class Login(Resource):
    '''
    API login
    '''

    # @api.expect(_auth)
    @api.expect(_auth_social_login)
    def post(self):
        """ Login user to the system.
        
        Args:
            access_token (string): the access_token get from login google on client.

        Returns:
            All information of user if he logged in and None if he did not log in.
        """

        post_data = request.json
        controller = AuthController()
        return controller.login_with_google(data=post_data)


@api.route('/logout')
class Logout(Resource):
    '''
    API logout
    '''

    @token_required
    def get(self):
        """ Logout the user from the system.
        
        Args:
            None

        Returns:
            None
        """

        # auth_header = request.headers.get('Authorization')
        # return ControllerAuth.logout_user(data=auth_header)
        # post_data = request.json
        controller = AuthController()
        return controller.logout_user(req=request)


@api.route('/info')
class UserInfor(Resource):
    '''
    Get user information. After user logging in successfully, user will get token, and this token will be used to get information.
    '''

    @token_required
    @api.response(code=200, model=_user_info, description='Model for user information.')
    def get(self):
        """ Get all user's information.
        
        Args:
            None

        Returns:
            User's information.
        """

        controller = AuthController()
        return controller.get_user_info(request)
        # return AuthController.get_logged_user(request)
