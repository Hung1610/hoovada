#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.topic.topic_controller import TopicController
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
topic_endorse_user_request = TopicDto.topic_endorse_user_request
upload_parser = TopicDto.upload_parser
endorsed_user_dto = TopicDto.model_user
get_endorsed_users_parser = TopicDto.get_endorsed_users_parser()


@api.route('/<string:topic_id_or_slug>/file')
@api.doc(params={'topic_id_or_slug': 'The topic id or slug'})
class TopicFile(Resource):
    @token_required
    @api.expect(upload_parser)
    @api.response(code=200, model=topic_response, description='Model for answer response.')
    def post(self, topic_id_or_slug):
        """Create media for topic by topic Id or slug"""
        
        controller = TopicController()
        return controller.create_with_file(object_id=topic_id_or_slug)


@api.route('')
class TopicList(Resource):
    @api.expect(parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """ Get list of topics satisfying query params """

        args = parser.parse_args()
        controller = TopicController()
        return controller.get(args=args)


    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def post(self):
        """ Create new topic."""
        
        data = api.payload
        controller = TopicController()
        return controller.create(data=data)

@api.deprecated
@api.route('/all/count')
@api.expect(parser)
class TopicListCount(Resource):
    def get(self):
        """Get count of topics satisfying query params """

        args = parser.parse_args()
        controller = TopicController()
        return controller.get_count(args=args)


@api.route('/<string:topic_id_or_slug>')
class Topic(Resource):
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def get(self, topic_id_or_slug):
        """ Get topic by topic Id or slug"""

        controller = TopicController()
        return controller.get_by_id(object_id=topic_id_or_slug)

    @token_required
    @api.expect(topic_request)
    @api.response(code=200, model=topic_response, description='Model for success response.')
    def patch(self, topic_id_or_slug):
        """Update existing topic by topic Id or slug"""

        data = api.payload
        controller = TopicController()
        return controller.update(object_id=topic_id_or_slug, data=data)


    @admin_token_required()
    def delete(self, topic_id_or_slug):
        """ Delete topic by topic Id or slug"""

        controller = TopicController()
        return controller.delete(object_id=topic_id_or_slug)


@api.route('/<string:topic_id_or_slug>/sub_topics')
class SubTopic(Resource):
    @api.response(code=200, model=topic_response, description='Get sub topics')
    def get(self, topic_id_or_slug):
        """ Get sub-topics of fixed-topics by fix_topic Id or slug"""

        controller = TopicController()
        return controller.get_sub_topics(object_id=topic_id_or_slug)


@api.route('/<string:topic_id_or_slug>/endorsed_users')
class EndorseUserTopic(Resource):
    @api.expect(get_endorsed_users_parser)
    @api.response(code=200, model=endorsed_user_dto, description='Endorsed users')
    def get(self, topic_id_or_slug):
        """ Get endorsed users for topic by topic Id or slug"""

        args = get_endorsed_users_parser.parse_args()
        controller = TopicController()
        return controller.get_endorsed_users(object_id=topic_id_or_slug, args=args)

    @token_required
    @api.expect(topic_endorse_user_request)
    @api.response(code=200, model=endorsed_user_dto, description='Endorsed users')
    def post(self, topic_id_or_slug):
        """ Create endorsed users for topic by topic Id or slug"""

        data = api.payload
        controller = TopicController()
        return controller.create_endorsed_users(object_id=topic_id_or_slug, data=data)


@api.route('/<string:topic_id_or_slug>/endorsed_users/<int:user_id>')
class EndorseUserTopicDelete(Resource):
    @token_required
    def delete(self, topic_id_or_slug, user_id):
        """ Delete endorsed users for topic by topic Id or slug"""
        
        controller = TopicController()
        return controller.delete_endorsed_users(object_id=topic_id_or_slug, user_id=user_id)


@api.route('/<string:topic_id_or_slug>/bookmarked_users')
class BookmarkUserTopic(Resource):
    @api.expect(get_endorsed_users_parser)
    @api.response(code=200, model=endorsed_user_dto, description='Bookmarked users')
    def get(self, topic_id_or_slug):
        """ Get endorsed users for topic by topic Id or slug"""

        args = get_endorsed_users_parser.parse_args()
        controller = TopicController()
        return controller.get_bookmarked_users(object_id=topic_id_or_slug, args=args)


@api.route('/create_fixed_topics')
class CreateFixedTopic(Resource):
    @admin_token_required()
    def post(self):
        """ Create fixed topics"""

        controller = TopicController()
        return controller.create_fixed_topics()


@api.deprecated
@api.route('/update_slug', doc=False)
class UpdateTopicSlug(Resource):
    @admin_token_required()
    def post(self):
        """Update Slug for topics """

        controller = TopicController()
        return controller.update_slug()


@api.deprecated
@api.route('/update_color', doc=False)
class UpdateTopicColor(Resource):
    @admin_token_required()
    def post(self):
        """Randomize color for fix topics"""

        controller = TopicController()
        return controller.update_color()


@api.route('/<string:topic_id_or_slug>/recommended-users')
class TopicRecommendedUsers(Resource):
    @api.expect(TopicDto.model_recommended_users_args_parser)
    @api.response(code=200, model=TopicDto.model_recommended_users_response, description='Model for recommended users response.')
    def get(self, topic_id_or_slug):
        """ Get recommended good users for given topic id or name"""

        args = TopicDto.model_recommended_users_args_parser.parse_args()
        controller = TopicController()
        return controller.get_recommended_users(object_id=topic_id_or_slug, args=args)


@api.route('/recommended-topics')
class RecommendedTopics(Resource):
    @api.expect(TopicDto.model_recommended_topics_parser)
    @api.response(code=200, model=topic_response, description='Model for topic response.')
    def get(self):
        """ Get recommended topics based on title."""

        args = TopicDto.model_recommended_topics_parser.parse_args()
        controller = TopicController()
        return controller.get_recommended_topics(args=args)
