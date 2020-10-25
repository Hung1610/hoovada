#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from common.decorator import token_required
from app.modules.user.ban.ban_dto import UserBanDto
from app.modules.user.ban.ban_controller import UserBanController
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = UserBanDto.api
_ban_request = UserBanDto.model_request
_ban_response = UserBanDto.model_response
_ban_get_params = UserBanDto.model_get_parser

@api.route('/all/ban')
class BanUserAll(Resource):
    @api.expect(_ban_get_params)
    def get(self):
        """
        Search all ban that satisfy conditions.
        """

        args = _ban_get_params.parse_args()
        controller = UserBanController()
        return controller.get(args=args)

@api.route('/all/ban/<int:object_id>')
class BanUserDetail(Resource):
    @api.expect(_ban_get_params)
    def get(self, object_id):
        """
        Get ban by ban id.
        """

        controller = UserBanController()
        return controller.get_by_id(object_id=object_id)

    @token_required
    def delete(self, object_id):
        """
        Delete ban by ban id.
        """
        
        controller = UserBanController()
        return controller.delete(object_id=object_id)

@api.route('/<int:user_id>/ban')
class BanUser(Resource):
    @token_required
    @api.response(code=200, model=_ban_response, description='The model for ban.')
    def post(self, user_id):
        """
        Create a ban on current user.
        """

        controller = UserBanController()
        data = api.payload
        return controller.create(user_id=user_id, data=data)
