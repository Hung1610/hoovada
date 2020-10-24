#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.common.decorator import token_required
from app.modules.q_a.answer.bookmark.bookmark_dto import AnswerBookmarkDto
from app.modules.q_a.answer.bookmark.bookmark_controller import AnswerBookmarkController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerBookmarkDto.api
_bookmark_request = AnswerBookmarkDto.model_request
_bookmark_response = AnswerBookmarkDto.model_response
_vote_get_params = AnswerBookmarkDto.model_get_parser

@api.route('/all/bookmark')
class BookmarkAnswerAll(Resource):
    @api.expect(_vote_get_params)
    def get(self, answer_id):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = AnswerBookmarkController()
        return controller.get(answer_id=None, args=args)

@api.route('/<int:answer_id>/bookmark')
class BookmarkAnswer(Resource):
    @api.expect(_vote_get_params)
    def get(self, answer_id):
        """
        Search all bookmark that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = AnswerBookmarkController()
        return controller.get(answer_id=answer_id, args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, answer_id):
        """
        Create a bookmark on current user.
        """

        controller = AnswerBookmarkController()
        return controller.create(answer_id=answer_id)

    @token_required
    def delete(self, answer_id):
        """
        Delete bookmark on current user.
        """
        
        controller = AnswerBookmarkController()
        return controller.delete(answer_id=answer_id)
