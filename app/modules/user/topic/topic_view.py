#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.topic.topic_controller import TopicController
from app.modules.user.topic.topic_dto import TopicDto
from common.utils.decorator import token_required


api = TopicDto.api
topic_response = TopicDto.model_response
topic_request = TopicDto.model_request
get_parser = TopicDto.model_get_parser
get_endorsed_topics_parser = TopicDto.get_endorsed_topics_parser()

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/me/topic')
class TopicMeList(Resource):
    @token_required
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """Get all user topic information of logged-in user"""

        args = get_parser.parse_args()
        controller = TopicController()
        user_id = g.current_user.id

        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def post(self):
        """Create user topic information of logged-in user"""

        data = api.payload
        controller = TopicController()
        user_id = g.current_user.id
        return controller.create(data=data, user_id=user_id)


@api.route('/<int:user_id>/topic')
class TopicList(Resource):
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self, user_id):
        """Create all user topic information by user_id"""

        args = get_parser.parse_args()
        controller = TopicController()
        return controller.get(user_id=user_id, args=args)


@api.route('/all/topic/<int:id>')
class TopicAll(Resource):

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def patch(self, id):
        """Update existing user topic information by user topic ID"""
        data = api.payload
        controller = TopicController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete existing user topic by user topic ID."""

        controller = TopicController()
        return controller.delete(object_id=id)

@api.deprecated
@api.route('/<int:user_id>/endorsed-topics')
class EndorsedTopicList(Resource):
    @api.expect(get_endorsed_topics_parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self, user_id):
        """Get all topics that satisfy conditions."""
        
        args = get_endorsed_topics_parser.parse_args()
        controller = TopicController()
        return controller.get_endorsed_topics(user_id=user_id, args=args)
