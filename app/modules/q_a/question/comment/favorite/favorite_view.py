#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.question.comment.favorite.favorite_dto import QuestionCommentFavoriteDto
from app.modules.q_a.question.comment.favorite.favorite_controller import QuestionCommentFavoriteController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionCommentFavoriteDto.api
_favorite_request = QuestionCommentFavoriteDto.model_request
_favorite_response = QuestionCommentFavoriteDto.model_response
_vote_get_params = QuestionCommentFavoriteDto.model_get_parser

@api.route('/<int:question_comment_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_vote_get_params)
    def get(self, question_comment_id):
        """
        Search all favorite that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = QuestionCommentFavoriteController()
        return controller.get(question_comment_id=question_comment_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, question_comment_id):
        """
        Create a favorite on current user.
        """

        controller = QuestionCommentFavoriteController()
        return controller.create(question_comment_id=question_comment_id)

    @token_required
    def delete(self, question_comment_id):
        """
        Delete favorite on current user.
        """
        
        controller = QuestionCommentFavoriteController()
        return controller.delete(question_comment_id=question_comment_id)
