
from flask import request
from werkzeug.datastructures import FileStorage

from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto
from app.user.user_controller import UserController
from app.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = UserDto.api
user_request = UserDto.model_request
user_response = UserDto.model_response


@api.route('')
class UserList(Resource):
    @admin_token_required
    # @api.marshal_list_with(_user)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self):
        """ Returns all users in the system.

        Returns
            List of users.
        """
        controller = UserController()
        return controller.get()

    @admin_token_required
    @api.expect(user_request)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def post(self):
        '''Create new user.
        Args:
            All data to create a new user is stored in dictionary form.

        Returns:
             New user is created successfully and error vice versa.
        '''
        data = api.payload
        controller = UserController()
        return controller.create(data=data)


#@api.route('/<int:id>')
@api.route('/<string:user_name>')
class User(Resource):
    @token_required
    # @api.marshal_with(_user)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self, user_name):
        """Get all information for specific user with ID `id`
        
        Args:
            id (int): The ID of the user.

        Returns: 
            The user with given ID in dictionary form.
        """

        controller = UserController()
            # return controller.get_by_id(object_id=id)
        return controller.get_by_user_name(user_name)

    @token_required
    @api.expect(user_request)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def put(self, user_name):
        '''Update an existed user in the system.
        
        Args:
            user_name(string)

        Returns:
             The user data after updated.
        '''

        data = api.payload
        controller = UserController()
        return controller.update(user_name=user_name, data=data)

    @token_required
    def delete(self, id):
        ''' Delete the user with the user_name `user_name`
        
        Args:
            user_name (string): The user_name of the user to be deleted.

        Returns: 
            True if user delete successfully and False vice versa.
        '''
        controller = UserController()
        return controller.delete(user_name=user_name)


avatar_upload = api.parser()
avatar_upload.add_argument('avatar', location='files',type=FileStorage, required=True, help='The image file to upload')
avatar_download = api.parser()
avatar_download.add_argument('filename', type=str, required=True, help='The name of the avatar')


@api.route('/avatar')
class Avatar(Resource):
    # @token_required
    @api.expect(avatar_download)
    def get(self):
        '''
        Download  avatar.
        -----------------
        :return:
        '''
        controler = UserController()
        return controler.get_avatar()

    @token_required
    @api.expect(avatar_upload)
    def post(self):
        '''
        Upload avatar.
        -------------
        :return:
        '''
        args = avatar_upload.parse_args()
        controller = UserController()
        return controller.upload_avatar(args=args)
