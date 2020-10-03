#!/usr/bin/env python
# -*- coding: utf-8 -*-

#third-party modules
from flask import request
from werkzeug.datastructures import FileStorage

# own modules
from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto
from app.modules.user.user_controller import UserController
from app.modules.auth.decorator import admin_token_required, token_required
from app.utils.types import UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = UserDto.api
user_get_parser = UserDto.model_get_parser
user_request = UserDto.model_request
user_response = UserDto.model_response


@api.route('')
class UserList(Resource):
    @token_required
    @api.expect(user_get_parser)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self):
        """ 
        Returns all users in the system.
        """
        
        args = user_get_parser.parse_args()
        controller = UserController()
        return controller.get(args=args)

    @admin_token_required(role=[UserRole.SUPER_ADMIN])
    @api.expect(user_request)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def post(self):
        """
        Create new user.
        """

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
        """
        Get all information for specific user with ID `id`
        """

        controller = UserController()
            # return controller.get_by_id(object_id=id)
        return controller.get_by_user_name(user_name)

    @admin_token_required()
    @api.expect(user_request)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def put(self, user_name):
        """
        Update an existed user in the system.
        """

        data = api.payload
        controller = UserController()
        return controller.update(user_name=user_name, data=data)

    @admin_token_required(role=[UserRole.SUPER_ADMIN])
    def delete(self, user_name):
        """ 
        Delete the user with the user_name `user_name`
        """

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
        """
        Download  avatar.
        """

        controler = UserController()
        return controler.get_avatar()

    @token_required
    @api.expect(avatar_upload)
    def post(self):
        """
        Upload avatar.
        """
        
        args = avatar_upload.parse_args()
        controller = UserController()
        return controller.upload_avatar(args=args)


parser = api.parser()
parser.add_argument('page', type=int, required=False, help='Search user by page.')
parser.add_argument('per_page', type=int, required=False, help='Get record number on page.')

@api.route('/user_hot')
@api.expect(parser)
class UserHot(Resource):
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self):
        """ get users hot 
        """

        args = parser.parse_args()
        controller = UserController()
        return controller.get_user_hot(args)
