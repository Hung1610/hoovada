#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import current_app, request
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.topic.topic_controller import TopicController
from app.modules.user.topic.topic_dto import TopicDto
from common.utils.decorator import admin_token_required, token_required
from common.utils.response import send_error

api = TopicDto.api
topic_response = TopicDto.model_response
topic_request = TopicDto.model_request
get_parser = TopicDto.model_get_parser
get_endorsed_topics_parser = TopicDto.get_endorsed_topics_parser()

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/<int:user_id>/topic')
class TopicList(Resource):
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self, user_id):
        """
        Search all topics that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = TopicController()
        return controller.get(user_id=user_id, args=args)

    @admin_token_required()
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def post(self, user_id):
        """Create new topic.
        """
        data = api.payload
        controller = TopicController()
        return controller.create(data=data, user_id=user_id)


@api.route('/me/topic')
class TopicMeList(Resource):
    @token_required
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """Search all topics that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = TopicController()

        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id

        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def post(self):
        """Create new topic.

        :return: The new topic if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = TopicController()

        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id

        return controller.create(data=data, user_id=user_id)


@api.route('/all/topic')
class TopicAllList(Resource):
    @token_required
    @api.expect(get_parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """
        Get all topic.
        """
        args = get_parser.parse_args()
        controller = TopicController()
        return controller.get(args=args)


@api.route('/all/topic/<int:id>')
class TopicAll(Resource):
    @token_required
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self, id):
        """
        Get topic by its ID.

        :param id: The ID of the topic.

        :return: The topic with the specific ID.
        """
        controller = TopicController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def patch(self, id):
        """Update existing topic by its ID.
        """
        data = api.payload
        controller = TopicController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete topic by its ID.
        """
        controller = TopicController()
        return controller.delete(object_id=id)


@api.route('/<int:user_id>/endorsed-topics')
class EndorsedTopicList(Resource):
    @api.expect(get_endorsed_topics_parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self, user_id):
        """
        Search all topics that satisfy conditions.
        """
        args = get_endorsed_topics_parser.parse_args()
        controller = TopicController()
        return controller.get_endorsed_topics(user_id=user_id, args=args)
