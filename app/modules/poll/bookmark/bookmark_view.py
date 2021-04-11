#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.poll.bookmark.bookmark_controller import \
    PollBookmarkController
# own modules
# from common.decorator import token_required
from app.modules.poll.bookmark.bookmark_dto import PollBookmarkDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollBookmarkDto.api
_bookmark_request = PollBookmarkDto.model_request
_bookmark_response = PollBookmarkDto.model_response
_vote_get_params = PollBookmarkDto.model_get_parser

@api.route('/all/bookmark')
class BookmarkPollAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = PollBookmarkController()
        return controller.get(poll_id=None, args=args)

@api.route('/<int:poll_id>/bookmark')
class BookmarkPoll(Resource):
    @api.expect(_vote_get_params)
    def get(self, poll_id):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = PollBookmarkController()
        return controller.get(poll_id=poll_id, args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, poll_id):
        """
        Create a bookmark on current user.
        """

        controller = PollBookmarkController()
        return controller.create(poll_id=poll_id)

    @token_required
    def delete(self, poll_id):
        """
        Delete bookmark on current user.
        """
        
        controller = PollBookmarkController()
        return controller.delete(poll_id=poll_id)
