#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.favorite.favorite_controller import AnswerFavoriteController
from app.modules.q_a.answer.favorite.favorite_dto import AnswerFavoriteDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerFavoriteDto.api
_favorite_request = AnswerFavoriteDto.model_request
_favorite_response = AnswerFavoriteDto.model_response
_favorite_get_params = AnswerFavoriteDto.model_get_parser

#@api.route('/<int:answer_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_favorite_get_params)
    def get(self, answer_id):
        """ Get all favorite that satisfy conditions."""

        args = _favorite_get_params.parse_args()
        controller = AnswerFavoriteController()
        return controller.get(answer_id=answer_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, answer_id):
        """Create a favorite on current user.
        """

        controller = AnswerFavoriteController()
        return controller.create(answer_id=answer_id)

    @token_required
    def delete(self, answer_id):
        """Delete favorite on current user"""
        
        controller = AnswerFavoriteController()
        return controller.delete(answer_id=answer_id)
