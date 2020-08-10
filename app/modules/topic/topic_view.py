#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.topic.topic_dto import TopicDto
from app.modules.topic.topic_controller import TopicController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicDto.api
topic_request = TopicDto.model_topic_request
topic_response = TopicDto.model_topic_response


@api.route('')
class TopicList(Resource):
    # @admin_token_required
    # @api.marshal_list_with(topic_response)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """
        Get list of topics from database.

        :return: The list of topics.
        """
        controller = TopicController()
        return controller.get()

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def post(self):
        """
        Create new topic.

        :return: The new topic if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = TopicController()
        return controller.create(data=data)


# @api.route('/fixed_topic')
# class FixedTopicList(Resource):
#     def get(self):
#

@api.route('/<int:id>')
class Topic(Resource):
    @token_required
    # @api.marshal_with(topic)
    @api.response(code=200, model=topic_response, description='Model for success response.')
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
    # @api.marshal_with(topic)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def put(self, id):
        """
        Update existing topic by its ID.

        :param id: The ID of the topic which need to be updated.

        :return: The updated topic if success and null vice versa.
        """
        data = api.payload
        controller = TopicController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete topic by its ID.

        :param id: The ID of the topic.

        :return:
        """
        controller = TopicController()
        return controller.delete(object_id=id)


@api.route('/<int:topic_id>/sub_topics')
class SubTopic(Resource):
    @token_required
    # @api.param(name='topic_id', description='The ID of fixed topic.')
    @api.response(code=200, model=topic_response, description='Get sub topics')
    def get(self, topic_id):
        """
        Get sub-topics of fixed-topics.

        :param topic_id: The ID of fixed topic to get sub-topics.

        :return:
        """
        controller = TopicController()
        return controller.get_sub_topics(fixed_topic_id=topic_id)


@api.route('/create_topics')
class CreateFixedTopic(Resource):
    def get(self):
        """
        Create fixed topics
        :return:
        """
        controller = TopicController()
        return controller.create_topics()


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=False, help='The name of the topic')
parser.add_argument('user_id', type=int, required=False, help='Search topic by user_id (who created topic)')
parser.add_argument('parent_id', type=int, required=False, help='Search all sub-topics which belongs to the parent ID.')
parser.add_argument('is_fixed', type=int, required=False, help='Get all fixed topics in database.')


@api.route('/search')
@api.expect(parser)
class TopicSearch(Resource):
    #@token_required
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def get(self):
        """
        Search all topics that satisfy conditions.
        ---------------------
        :name: The name of the topics to search

        :user_id: Search topic by user_id (who created topics)

        :parent_id: Search all topics by their parent topic ID.

        :return: List of buyers
        """
        args = parser.parse_args()
        controller = TopicController()
        return controller.search(args=args)
