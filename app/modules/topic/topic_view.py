#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.topic.topic_controller import TopicController
# own modules
# from common.decorator import token_required
from app.modules.topic.topic_dto import TopicDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicDto.api
parser = TopicDto.model_get_parser
topic_request = TopicDto.model_topic_request
topic_response = TopicDto.model_topic_response
endorsed_user_dto = TopicDto.model_endorsed_user
get_endorsed_users_parser = TopicDto.get_endorsed_users_parser()
topic_endorse_user_request = TopicDto.topic_endorse_user_request
upload_parser = TopicDto.upload_parser


@api.route('/<string:topic_id_or_slug>/file')
@api.doc(params={'topic_id_or_slug': 'The topic id or slug'})
class TopicFile(Resource):
    @admin_token_required()
    @api.expect(upload_parser)
    @api.response(code=200, model=topic_response, description='Model for answer response.')
    def post(self, topic_id_or_slug):
        """
        Create media for topic.
        """
        controller = TopicController()
        return controller.create_with_file(object_id=topic_id_or_slug)


@api.route('')
class TopicList(Resource):
    @api.expect(parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """ 
        Get list of topics from database.
        """

        args = parser.parse_args()
        controller = TopicController()
        return controller.get(args=args)


    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def post(self):
        """ 
        Create new topic.
        """
        
        data = api.payload
        controller = TopicController()
        return controller.create(data=data)


@api.route('/all/count')
@api.expect(parser)
class TopicListCount(Resource):
    def get(self):
        """ 
        Get list of topics from database.
        """

        args = parser.parse_args()
        controller = TopicController()
        return controller.get_count(args=args)


# @api.route('/fixed_topic')
# class FixedTopicList(Resource):
#     def get(self):
#

@api.route('/<string:topic_id_or_slug>')
class Topic(Resource):
    # @api.marshal_with(topic)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def get(self, topic_id_or_slug):
        """ 
        Get topic by its ID.
        """

        controller = TopicController()
        return controller.get_by_id(object_id=topic_id_or_slug)


    @token_required
    @api.expect(topic_request)
    # @api.marshal_with(topic)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def put(self, topic_id_or_slug):
        """ 
        Update existing topic by its ID.

        """

        data = api.payload
        controller = TopicController()
        return controller.update(object_id=topic_id_or_slug, data=data)

    @admin_token_required()
    def delete(self, topic_id_or_slug):
        """ 
        Delete topic by its ID.
        """

        controller = TopicController()
        return controller.delete(object_id=topic_id_or_slug)


@api.route('/<string:topic_id_or_slug>/sub_topics')
class SubTopic(Resource):
    # @api.param(name='topic_id_or_slug', description='The ID of fixed topic.')
    @api.response(code=200, model=topic_response, description='Get sub topics')
    def get(self, topic_id_or_slug):
        """ 
        Get sub-topics of fixed-topics.
        """

        controller = TopicController()
        return controller.get_sub_topics(object_id=topic_id_or_slug)


@api.route('/<string:topic_id_or_slug>/endorsed_users')
class EndorseUserTopic(Resource):
    @api.expect(get_endorsed_users_parser)
    @api.response(code=200, model=endorsed_user_dto, description='Endorsed users')
    def get(self, topic_id_or_slug):
        """ 
        Get endorsed users for topic.
        """

        args = get_endorsed_users_parser.parse_args()
        controller = TopicController()
        return controller.get_endorsed_users(object_id=topic_id_or_slug, args=args)

    @token_required
    @api.expect(topic_endorse_user_request)
    @api.response(code=200, model=endorsed_user_dto, description='Endorsed users')
    def post(self, topic_id_or_slug):
        """ 
        Create endorsed users for topic.
        """

        data = api.payload
        controller = TopicController()
        return controller.create_endorsed_users(object_id=topic_id_or_slug, data=data)

@api.route('/<string:topic_id_or_slug>/endorsed_users/<int:user_id>')
class EndorseUserTopicDelete(Resource):
    @token_required
    def delete(self, topic_id_or_slug, user_id):
        """ 
        Delete endorsed users for topic.
        """
        
        controller = TopicController()
        return controller.delete_endorsed_users(object_id=topic_id_or_slug, user_id=user_id)


@api.route('/<string:topic_id_or_slug>/bookmarked_users')
class BookmarkUserTopic(Resource):
    @api.expect(get_endorsed_users_parser)
    @api.response(code=200, model=endorsed_user_dto, description='Bookmarked users')
    def get(self, topic_id_or_slug):
        """ 
        Get endorsed users for topic.
        """

        args = get_endorsed_users_parser.parse_args()
        controller = TopicController()
        return controller.get_bookmarked_users(object_id=topic_id_or_slug, args=args)


@api.route('/create_topics')
class CreateFixedTopic(Resource):
    @admin_token_required()
    def post(self):
        """ 
        Create fixed topics
        """

        controller = TopicController()
        return controller.create_fixed_topics()

@api.deprecated
@api.route('/update_slug', doc=False)
class UpdateTopicSlug(Resource):
    @admin_token_required()
    def post(self):
        """
        Update Slug for topics in DB
        """

        controller = TopicController()
        return controller.update_slug()

@api.deprecated
@api.route('/update_color', doc=False)
class UpdateTopicColor(Resource):
    @admin_token_required()
    def post(self):
        """
        Randomize color for fix topics
        """

        controller = TopicController()
        return controller.update_color()