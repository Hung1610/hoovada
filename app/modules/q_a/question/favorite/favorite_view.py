#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from common.decorator import token_required
from app.modules.q_a.question.favorite.favorite_dto import QuestionFavoriteDto
from app.modules.q_a.question.favorite.favorite_controller import QuestionFavoriteController
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionFavoriteDto.api
_favorite_request = QuestionFavoriteDto.model_request
_favorite_response = QuestionFavoriteDto.model_response
_vote_get_params = QuestionFavoriteDto.model_get_parser


@api.route('/<int:question_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_vote_get_params)
    def get(self, question_id):
        """
        Search all favorite that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = QuestionFavoriteController()
        return controller.get(question_id=question_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, question_id):
        """
        Create a favorite on current user.
        """

        controller = QuestionFavoriteController()
        return controller.create(question_id=question_id)

    @token_required
    def delete(self, question_id):
        """
        Delete favorite on current user.
        """
        
        controller = QuestionFavoriteController()
        return controller.delete(question_id=question_id)
