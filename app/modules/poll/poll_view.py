#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.poll.poll_controller import PollController
from app.modules.poll.poll_dto import PollDto
from common.cache import cache
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollDto.api
poll_response = PollDto.model_response
poll_request = PollDto.model_request
get_parser = PollDto.get_parser

@api.route('')
class PollList(Resource):
    @token_required
    @api.expect(get_parser)
    @api.response(code=200, model=poll_response, description='Model for poll response.')
    def get(self):
        """Get poll(s) by params"""

        controller = PollController()
        args = get_parser.parse_args()
        return controller.get(args=args)


    @token_required
    @api.expect(poll_request)
    def post(self):
        """Create new poll."""

        data = api.payload
        controller = PollController()
        return controller.create(data=data)


@api.route('/<string:id_or_slug>')
class Poll(Resource):
    @token_required
    @api.response(code=200, model=poll_response, description='Model for poll response.')
    def get(self, id_or_slug):
        """ Get specific poll by poll Id or slug"""

        controller = PollController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(poll_request)
    def patch(self, id_or_slug):
        """Update the existing poll by poll id or slug"""

        data = api.payload
        controller = PollController()
        result = controller.update(object_id=id_or_slug, data=data)
        return result

    @token_required
    def delete(self, id_or_slug):
        """Delete existing poll by poll id or slug"""

        controller = PollController()
        result = controller.delete(object_id=id_or_slug)
        return result