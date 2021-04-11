#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.poll.poll_select.poll_select_controller import PollSelectController
from app.modules.poll.poll_select.poll_select_dto import PollSelectDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollSelectDto.api
poll_select_response = PollSelectDto.model_response
poll_select_request = PollSelectDto.model_request
get_parser = PollSelectDto.get_parser


@api.route('/<string:id_or_slug>/select')
class PollSelectList(Resource):
    @api.response(code=200, model=poll_select_response, description='Model for poll select response.')
    #@cache.cached(query_string=True)
    def get(self, id_or_slug):
        """Get the list of poll selects from database.
        """

        args = get_parser.parse_args()
        controller = PollSelectController()
        return controller.get(poll_id=id_or_slug , args=args)

    @token_required
    @api.expect(poll_select_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=poll_select_response, description='Model for poll select response.')
    def post(self, id_or_slug):
        """
        Create new poll select.
        """

        data = api.payload
        controller = PollSelectController()
        return controller.create(data=data, poll_id=id_or_slug)

@api.route('/all/select/<int:poll_select_id>')
class PollSelect(Resource):
    @token_required
    @api.expect(poll_select_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=poll_select_response, description='Model for poll select response.')
    def put(self, poll_select_id):
        """
        Update existing poll select.
        """

        data = api.payload
        controller = PollSelectController()
        return controller.update(object_id=poll_select_id, data=data)

    @token_required
    def delete(self, poll_select_id):
        """Delete existing poll select by poll select id"""

        controller = PollSelectController()
        result = controller.delete(object_id=poll_select_id)
        return result