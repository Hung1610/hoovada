#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from common.decorator import token_required
from app.modules.topic.bookmark.bookmark_dto import TopicBookmarkDto
from app.modules.topic.bookmark.bookmark_controller import TopicBookmarkController
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicBookmarkDto.api
_bookmark_request = TopicBookmarkDto.model_request
_bookmark_response = TopicBookmarkDto.model_response
_vote_get_params = TopicBookmarkDto.model_get_parser

@api.route('/all/bookmark')
class BookmarkTopicAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = TopicBookmarkController()
        return controller.get(topic_id=None, args=args)

@api.route('/<int:topic_id>/bookmark')
class BookmarkTopic(Resource):
    @api.expect(_vote_get_params)
    def get(self, topic_id):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = TopicBookmarkController()
        return controller.get(topic_id=topic_id, args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, topic_id):
        """
        Create a bookmark on current user.
        """

        controller = TopicBookmarkController()
        return controller.create(topic_id=topic_id)

    @token_required
    def delete(self, topic_id):
        """
        Delete bookmark on current user.
        """
        
        controller = TopicBookmarkController()
        return controller.delete(topic_id=topic_id)
