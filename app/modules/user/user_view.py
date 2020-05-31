from flask import request
from werkzeug.datastructures import FileStorage

from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto
from .user_controller import UserController
from ..auth.decorator import admin_token_required, token_required

api = UserDto.api
_user = UserDto.model


@api.route('')
class UserList(Resource):
    @admin_token_required
    # @api.marshal_list_with(_user)
    def get(self):
        """
        Returns all users in the system.
        ------------------

        :return List of users.
        """
        controller = UserController()
        return controller.get()

    @admin_token_required
    # @api.expect(_user)
    def post(self):
        '''
        Create new user.
        -------------------
        All data to create a new user is stored in dictionary form.

        :return: New user is created successfully and error vice versa.
        '''
        data = api.payload
        controller = UserController()
        return controller.create(data=data)


@api.route('/<int:id>')
class User(Resource):
    @token_required
    # @api.marshal_with(_user)
    def get(self, id):
        """``
        Get all information for specific user with ID `id`
        -------------------

        :param id: The ID of the user.

        :return: The user with given ID in dictionary form.
        """
        controller = UserController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(_user, validate=True)
    def put(self, id):
        '''
        Update an existed user in the system.
        --------------------
        :param id:

        :return:
        '''
        data = api.payload
        controller = UserController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete the user with the ID `id`
        -----------------

        :param id: The ID of the user to be deleted.

        :return: True if user delete successfully and False vice versa.
        '''
        controller = UserController()
        return controller.delete(object_id=id)


avatar_upload = api.parser()
avatar_upload.add_argument('avatar', location='files',
                           type=FileStorage, required=True, help='The image file to upload')

avatar_download = api.parser()
avatar_download.add_argument('filename', type=str, required=True, help='The name of the avatar')


@api.route('/avatar')
class UploadAvatar(Resource):
    @token_required
    @api.expect(avatar_download)
    def get(self):
        controler = UserController()
        return controler.get_avatar()

    @token_required
    @api.expect(avatar_upload)
    def post(self):
        args = avatar_upload.parse_args()
        controller = UserController()
        return controller.upload_avatar(args=args)
