from flask import request

from app.modules.auth.auth_controller import AuthController
from app.modules.auth.auth_dto import AuthDto
from app.modules.common.view import Resource

api = AuthDto.api
_auth = AuthDto.model


@api.route('/register')
class Register(Resource):
    '''

    '''
    def post(self):
        post_data = request.json
        return AuthController.register(post_data)

@api.route('/activate')
class ConfirmEmail(Resource):
    def post(self):
        pass

@api.route('/login')
class Login(Resource):
    '''
    API login
    '''

    @api.expect(_auth)
    def post(self):
        """
        Login user to the system.
        -------------
        :param email: the email of the user.
        :param password: the password of the user.

        :return: All information of user if he logged in and None if he did not log in.
        """
        post_data = request.json
        return AuthController.login_user(data=post_data)


@api.route('/logout')
class Logout(Resource):
    '''
    API logout
    '''

    @api.expect(_auth)
    def post(self):
        """
        Logout the user from the system.
        -------------

        :return:
        """
        # auth_header = request.headers.get('Authorization')
        # return ControllerAuth.logout_user(data=auth_header)
        post_data = request.json
        return AuthController.logout_user(data=post_data)


@api.route('/info')
class UserInfor(Resource):
    '''
    API User's information.
    '''

    def get(self):
        """
        Trả lại các thông tin về role của người dùng, order tương ứng.
        :return:
        """
        return AuthController.get_logged_user(request)
