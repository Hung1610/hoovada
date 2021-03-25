#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.question.bookmark.bookmark_controller import QuestionBookmarkController
from app.modules.q_a.question.bookmark.bookmark_dto import QuestionBookmarkDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionBookmarkDto.api
_bookmark_request = QuestionBookmarkDto.model_request
_bookmark_response = QuestionBookmarkDto.model_response
_vote_get_params = QuestionBookmarkDto.model_get_parser



@api.route('/all/bookmark')
class BookmarkQuestionAll(Resource):
    @api.expect(_vote_get_params)
    def get(self, question_id):
        """Get all bookmark that satisfy conditions"""

        args = _vote_get_params.parse_args()
        controller = QuestionBookmarkController()
        return controller.get(args=args)


@api.route('/<int:question_id>/bookmark')
class BookmarkQuestion(Resource):
    @api.expect(_vote_get_params)
    def get(self, question_id):
        """Get all bookmark of a particular question"""

        args = _vote_get_params.parse_args()
        args['question_id'] = question_id
        controller = QuestionBookmarkController()
        return controller.get(args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, question_id):
        """Create a bookmark on current user"""

        controller = QuestionBookmarkController()
        return controller.create(question_id=question_id)

    @token_required
    def delete(self, question_id):
        """Delete bookmark on current user"""
        
        controller = QuestionBookmarkController()
        return controller.delete(question_id=question_id)
