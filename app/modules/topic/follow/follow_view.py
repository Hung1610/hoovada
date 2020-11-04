#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.topic.follow.follow_controller import TopicFollowController
# own modules
# from common.decorator import token_required
from app.modules.topic.follow.follow_dto import TopicFollowDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicFollowDto.api
_follow_request = TopicFollowDto.model_request
_follow_response = TopicFollowDto.model_response
_vote_get_params = TopicFollowDto.model_get_parser

@api.route('/all/follow')
class FollowTopicAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """
        Search all follow that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = TopicFollowController()
        return controller.get(topic_id=None, args=args)


@api.route('all/follow/<int:object_id>')
class FollowTopicAllDetail(Resource):
    @admin_token_required
    def delete(self, object_id):
        """
        Delete follow.
        """
        
        controller = TopicFollowController()
        return controller.delete(object_id=object_id)


@api.route('/<int:topic_id>/follow')
class FollowTopic(Resource):
    @api.expect(_vote_get_params)
    def get(self, topic_id):
        """
        Search all follow that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = TopicFollowController()
        return controller.get(topic_id=topic_id, args=args)

    @token_required
    @api.response(code=200, model=_follow_response, description='The model for follow.')
    def post(self, topic_id):
        """
        Create a follow on current user.
        """

        controller = TopicFollowController()
        return controller.create(topic_id=topic_id)

    @token_required
    def delete(self, topic_id):
        """
        Delete follow on current user.
        """
        
        controller = TopicFollowController()
        return controller.delete_for_current_user(topic_id=topic_id)
