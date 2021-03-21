#!/usr/bin/env python
# -*- coding: utf-8 -*-

#third-party modules
from flask import request
from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

from app.modules.user.user_controller import UserController
from app.modules.user.user_dto import UserDto
from common.utils.decorator import admin_token_required, token_required
from common.utils.types import UserRole
# own modules
from common.view import Resource

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = UserDto.api
user_get_parser = UserDto.model_get_parser
user_get_social_parser = UserDto.model_get_social_account_parser
user_request = UserDto.model_request
user_response = UserDto.model_response


@api.route('')
class UserList(Resource):
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
    @api.expect(user_request, validate=True)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def post(self):
        """
        Create new user.
        """

        data = api.payload
        controller = UserController()
        return controller.create(data=data)


@api.route('/<int:user_id>/feed')
# @api.expect(user_get_parser)
@api.response(code=200, description='Model for user response.')
class UserGetFeed(Resource):
    def get(self, user_id):
        """
        Get user's feed
        """

        # args = user_get_parser.parse_args()
        controller = UserController()
        return controller.get_feed(user_id=user_id)


@api.route('/all/count')
@api.expect(user_get_parser)
class UserListCount(Resource):
    def get(self):
        """ 
        Get list of topics from database.
        """

        args = user_get_parser.parse_args()
        controller = UserController()
        return controller.get_count(args=args)


@api.route('/<string:user_name>/social')
class UserSocialAccount(Resource):
    @api.expect(user_get_social_parser)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self, user_name):
        """
        Get all information for specific user with ID `id`
        """

        controller = UserController()
        args = user_get_social_parser.parse_args()
        return controller.get_social_account(user_name, args)


#@api.route('/<int:id>')
@api.route('/<string:user_name>')
class User(Resource):
    # @api.marshal_with(_user)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self, user_name):
        """
        Get all information for specific user with ID `id`
        """

        controller = UserController()
            # return controller.get_by_id(object_id=id)
        return controller.get_by_user_name(user_name)

    @api.expect(user_request, validate=True)
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
avatar_upload.add_argument('avatar', location='files',type=FileStorage, required=False, help='The image file to upload')
@api.route('/avatar')
class UserAvatar(Resource):
    @token_required
    @api.expect(avatar_upload)
    def post(self):
        """
        Upload avatar.
        """
        
        args = avatar_upload.parse_args()
        controller = UserController()
        return controller.upload_avatar(args=args)


cover_upload = api.parser()
cover_upload.add_argument('cover', location='files',type=FileStorage, required=False, help='The image file to upload')
@api.route('/cover')
class UserCover(Resource):
    @token_required
    @api.expect(cover_upload)
    def post(self):
        """
        Upload cover.
        """
        
        args = cover_upload.parse_args()
        controller = UserController()
        return controller.upload_cover(args=args)


doc_upload = api.parser()
doc_upload.add_argument('doc', location='files',type=FileStorage, required=False, help='The image file to upload')
@api.route('/doc')
class UserDoc(Resource):
    @token_required
    @api.expect(doc_upload)
    def post(self):
        """
        Upload doc.
        """
        
        args = doc_upload.parse_args()
        controller = UserController()
        return controller.upload_document(args=args)
