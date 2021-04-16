#!/usr/bin/env python
# -*- coding: utf-8 -*-

#third-party modules
from flask import request
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
user_mention_request = UserDto.model_user_mention_request


@api.route('')
class UserList(Resource):
    @api.expect(user_get_parser)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self):
        """ Returns all users in the system"""
        
        args = user_get_parser.parse_args()
        controller = UserController()
        return controller.get(args=args)

    @admin_token_required(role=[UserRole.SUPER_ADMIN])
    @api.expect(user_request, validate=True)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def post(self):
        """Create new user - used by Super Admin"""

        data = api.payload
        controller = UserController()
        return controller.create(data=data)


@api.route('/mention')
@api.expect(user_mention_request)
@api.response(code=200, description='Model for notify that user has been mentioned.')
class UserMention(Resource):
    @token_required
    def post(self):
        """Notify that user has been mentioned"""

        args = user_mention_request.parse_args()
        controller = UserController()
        return controller.notify_user_mention(args)


@api.route('/all/count')
@api.expect(user_get_parser)
class UserListCount(Resource):
    def get(self):
        """ Get list of topics """

        args = user_get_parser.parse_args()
        controller = UserController()
        return controller.get_count(args=args)


@api.route('/<string:user_name>/social')
class UserSocialAccount(Resource):
    @api.expect(user_get_social_parser)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self, user_name):
        """Get all information for specific user with ID `id`"""

        controller = UserController()
        args = user_get_social_parser.parse_args()
        return controller.get_social_account(user_name, args)


#@api.route('/<int:id>')
@api.route('/<string:user_name>')
class User(Resource):
    @api.response(code=200, model=user_response, description='Model for user response.')
    def get(self, user_name):
        """Get all information for specific user with ID `id`"""

        controller = UserController()
        return controller.get_by_user_name(user_name)

    @api.expect(user_request, validate=True)
    @api.response(code=200, model=user_response, description='Model for user response.')
    def put(self, user_name):
        """Update an existed user in the system"""

        data = api.payload
        controller = UserController()
        return controller.update(user_name=user_name, data=data)

    @admin_token_required(role=[UserRole.SUPER_ADMIN])
    def delete(self, user_name):
        """ Delete the user with the user_name `user_name`"""

        controller = UserController()
        return controller.delete(user_name=user_name)


avatar_upload = api.parser()
avatar_upload.add_argument('avatar', location='files',type=FileStorage, required=False, help='The image file to upload')
@api.route('/avatar')
class UserAvatar(Resource):
    @token_required
    @api.expect(avatar_upload)
    def post(self):
        """Upload avatar in profile home"""
        
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
        """Upload cover page in profile home"""
        
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
        """Upload doc to verify in settings"""
        
        args = doc_upload.parse_args()
        controller = UserController()
        return controller.upload_document(args=args)
