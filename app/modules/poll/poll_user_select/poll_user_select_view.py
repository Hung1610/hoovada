#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.poll.poll_user_select.poll_user_select_controller import PollUserSelectController
from app.modules.poll.poll_user_select.poll_user_select_dto import PollUserSelectDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollUserSelectDto.api
poll_user_select_response = PollUserSelectDto.model_response
poll_user_select_request = PollUserSelectDto.model_request
get_parser = PollUserSelectDto.get_parser


@api.route('/<string:poll_select_id>/user')
class PollUserSelectList(Resource):
    @api.response(code=200, model=poll_user_select_response, description='Model for poll user select response.')
    #@cache.cached(query_string=True)
    def get(self, poll_select_id):
        """Get the list of poll user selects from database.
        """

        args = get_parser.parse_args()
        controller = PollUserSelectController()
        return controller.get(poll_select_id=poll_select_id , args=args)


    @token_required
    # @api.marshal_with(answer)
    @api.response(code=200, model=poll_user_select_response, description='Model for poll user select response.')
    def post(self, poll_select_id):
        """
        Create new poll user select.
        """

        controller = PollUserSelectController()
        return controller.create(poll_select_id=poll_select_id)

@api.route('/all/user/<int:poll_user_select_id>')
class PollUserSelect(Resource):
    @token_required
    def delete(self, poll_user_select_id):
        """Delete existing poll user select by poll user select id"""

        controller = PollUserSelectController()
        result = controller.delete(object_id=poll_user_select_id)
        return result