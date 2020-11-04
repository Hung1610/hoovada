#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.article.voting.vote_controller import VoteController
# own modules
from app.modules.article.voting.vote_dto import VoteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = VoteDto.api
_vote_request_article = VoteDto.model_request_article
_vote_response = VoteDto.model_response
_vote_get_params = VoteDto.model_get_parser
        

@api.route('/<int:article_id>/vote')
class VoteArticle(Resource):
    @api.expect(_vote_get_params)
    def get(self, article_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = VoteController()
        return controller.get(article_id=article_id, args=args)

    @token_required
    @api.expect(_vote_request_article)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, article_id):
        """
        Create/Update current user vote on article.
        """

        controller = VoteController()
        data = api.payload
        return controller.create(article_id=article_id, data=data)

    @token_required
    def delete(self, article_id):
        """
        Delete current user vote on question.
        """
        
        controller = VoteController()
        return controller.delete(article_id=article_id)
