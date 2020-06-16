from flask import request

from app.modules.auth.auth_controller import AuthController
from app.modules.auth.auth_dto import AuthDto
from app.modules.auth.decorator import token_required
from app.modules.common.view import Resource

api = AuthDto.api
_auth = AuthDto.model
_auth_login = AuthDto.model_login


@api.route('/register')
class Register(Resource):
    '''
    Register new user.

    '''
    @api.expect(_auth)
    def post(self):
        '''
        Register new user.

        :param display_name: The name to display in website (optional).

        :param email: The email to register.

        :param password: The password to register.

        :return: En confirmation email will be sent to user's mailbox to activate account.
        '''
        post_data = request.json
        controller = AuthController()
        return controller.register(post_data)

@api.route('/resend_confirmation')
class ResendConfirmation(Resource):
    @api.expect(_auth_login)
    def post(self):
        '''
        Resend confirmation email.

        :return:
        '''
        data = api.payload
        controller = AuthController()
        return controller.resend_confirmation(data=data)

@api.route('/confirmation/<token>')
class ConfirmationEmail(Resource):
    def get(self, token):
        '''
        Check confirmation token.

        :param token: The token to confirm.

        :return:
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
        """
        Login user to the system.
        -------------
        :param email: the email of the user.
        :param password: the password of the user.

        :return: All information of user if he logged in and None if he did not log in.
        """
        post_data = request.json
        controller = AuthController()
        return controller.login_user(data=post_data)


@api.route('/logout')
class Logout(Resource):
    '''
    API logout
    '''
    # @api.expect(_auth_register)
    @token_required
    def get(self):
        """
        Logout the user from the system.
        -------------

        :return:
        """
        # auth_header = request.headers.get('Authorization')
        # return ControllerAuth.logout_user(data=auth_header)
        # post_data = request.json
        controller = AuthController()
        return controller.logout_user(req=request)


@api.route('/info')
class UserInfor(Resource):
    '''
    API to get user information.

    After user logging in successfully, user will get token, and this token will be used to get information.
    '''
    @token_required
    def get(self):
        """
        Get all user's information.

        :return: User's information.
        """
        controller = AuthController()
        return controller.get_user_info(request)
        # return AuthController.get_logged_user(request)
