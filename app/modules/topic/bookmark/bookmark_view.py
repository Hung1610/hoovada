#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.topic.bookmark.bookmark_controller import TopicBookmarkController
from app.modules.topic.bookmark.bookmark_dto import TopicBookmarkDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicBookmarkDto.api
_bookmark_request = TopicBookmarkDto.model_request
_bookmark_response = TopicBookmarkDto.model_response
_vote_get_params = TopicBookmarkDto.model_get_parser
_model_bookmark_multiple_topics_request = TopicBookmarkDto.model_bookmark_multiple_topics_request
_model_bookmark_multiple_topics_response = TopicBookmarkDto.model_bookmark_multiple_topics_response


@api.route('/all/bookmark')
class BookmarkTopicAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """Search all topic bookmark"""

        args = _vote_get_params.parse_args()
        controller = TopicBookmarkController()
        return controller.get(args=args)

    @token_required
    @api.expect(_model_bookmark_multiple_topics_request)
    def create(self):
        """Create multiple bookmarks for current user"""

        args = api.payload
        controller = TopicBookmarkController()
        return controller.create_multiple_topics_bookmarks(args=args)


@api.route('/<int:topic_id>/bookmark')
class BookmarkTopic(Resource):
    @api.expect(_vote_get_params)
    def get(self, topic_id):
        """Search all bookmarks from topic Id"""

        args = _vote_get_params.parse_args()
        args['topic_id'] = topic_id
        controller = TopicBookmarkController()
        return controller.get(args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, topic_id):
        """Create a bookmark on current user from topic id"""

        controller = TopicBookmarkController()
        return controller.create(topic_id=topic_id)

    @token_required
    def delete(self, topic_id):
        """Delete bookmark on current user from topic Id """
        
        controller = TopicBookmarkController()
        return controller.delete(topic_id=topic_id)
