#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.poll.poll_topic.poll_topic_controller import PollTopicController
from app.modules.poll.poll_topic.poll_topic_dto import PollTopicDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollTopicDto.api
poll_topic_response = PollTopicDto.model_response
poll_topic_request = PollTopicDto.model_request
get_parser = PollTopicDto.get_parser


@api.route('/<string:id_or_slug>/topic')
class PollTopicList(Resource):
    @api.response(code=200, model=poll_topic_response, description='Model for poll topic response.')
    #@cache.cached(query_string=True)
    def get(self, id_or_slug):
        """Get the list of poll topics from database.
        """

        args = get_parser.parse_args()
        controller = PollTopicController()
        return controller.get(poll_id=id_or_slug , args=args)


    @token_required
    @api.expect(poll_topic_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=poll_topic_response, description='Model for poll topic response.')
    def post(self, id_or_slug):
        """
        Create new poll topic.
        """

        data = api.payload
        controller = PollTopicController()
        return controller.create(data=data, poll_id=id_or_slug)

@api.route('/all/topic/<int:poll_topic_id>')
class PollTopic(Resource):
    @token_required
    def delete(self, poll_topic_id):
        """Delete existing poll topic by poll topic id"""

        controller = PollTopicController()
        result = controller.delete(object_id=poll_topic_id)
        return result