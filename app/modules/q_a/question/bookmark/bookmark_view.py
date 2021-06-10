#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.question.bookmark.bookmark_controller import QuestionBookmarkController
from app.modules.q_a.question.bookmark.bookmark_dto import QuestionBookmarkDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionBookmarkDto.api
MODEL_RESPONSE = QuestionBookmarkDto.model_response
MODEL_GET_PARSER = QuestionBookmarkDto.model_get_parser


@api.route('/all/bookmark')
class BookmarkQuestionAll(Resource):
    @api.expect(MODEL_GET_PARSER)
    @api.response(code=200, model=MODEL_RESPONSE, description='The model for bookmark.')
    def get(self):
        """Get all bookmark that satisfy conditions"""

        args = MODEL_GET_PARSER.parse_args()
        controller = QuestionBookmarkController()
        return controller.get(args=args)


@api.route('/<int:question_id>/bookmark')
class BookmarkQuestion(Resource):
    @api.expect(MODEL_GET_PARSER)
    @api.response(code=200, model=MODEL_RESPONSE, description='The model for bookmark.')
    def get(self, question_id):
        """Get all bookmark of a particular question"""

        args = MODEL_GET_PARSER .parse_args()
        args['question_id'] = question_id
        controller = QuestionBookmarkController()
        return controller.get(args=args)

    @token_required
    def post(self, question_id):
        """Create a bookmark on current user using quesion_id"""

        controller = QuestionBookmarkController()
        return controller.create(object_id=question_id)

    @token_required
    def delete(self, question_id):
        """Delete bookmark on current user using quesion_id"""
        
        controller = QuestionBookmarkController()
        return controller.delete(object_id=question_id)
