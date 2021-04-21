#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

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
get_parser = PollUserSelectDto.get_parser


@api.route('/<string:poll_select_id>/user')
class PollUserSelectList(Resource):
    @api.expect(get_parser)
    @api.response(code=200, model=poll_user_select_response, description='Model for getting poll user select response.')
    #@cache.cached(query_string=True)
    def get(self, poll_select_id):
        """Get a poll user selects from database"""

        args = get_parser.parse_args()
        controller = PollUserSelectController()
        return controller.get(poll_select_id=poll_select_id , args=args)


    @token_required
    @api.response(code=200, model=poll_user_select_response, description='Model for posting poll user select response.')
    def post(self):
        """Create a a poll select"""

        data = api.payload
        controller = PollUserSelectController()
        return controller.create(data=data)


@api.route('/user/<int:poll_user_select_id>')
class PollUserSelect(Resource):
    @token_required
    def delete(self, poll_user_select_id):
        """Delete existing poll user select by poll user select id"""

        controller = PollUserSelectController()
        result = controller.delete(object_id=poll_user_select_id)
        return result