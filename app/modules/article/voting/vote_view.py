#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.voting.vote_dto import VoteDto
from app.modules.article.voting.vote_controller import VoteController
from app.modules.auth.decorator import admin_token_required, token_required

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
    @token_required
    @api.expect(_vote_get_params)
    def get(self, article_id):
        """
        Search all votes that satisfy conditions.
        ---------------------

        :user_id: Search votes by user_id

        :article_id: Search all votes by article ID.

        :from_date: Search votes by from date.

        :to_date: Search votes by to date.

        :return: List of comments.
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

        :return:
        """
        controller = VoteController()
        data = api.payload
        return controller.create(article_id=article_id, data=data)

<<<<<<< HEAD
@api.route('/<int:article_id>/vote/<int:user_id>')
class VoteArticleById(Resource):
    @token_required
    # @api.marshal_with(vote)
    def get(self, article_id, user_id):
        """
        Get vote by article ID and user ID.

        :param id: The ID of the vote.

        :return: The vote with the specific ID.
        """
        controller = VoteController()
        return controller.get_by_id(article_id=article_id, user_id=user_id)

    @token_required
    def delete(self, article_id, user_id):
        """
        Delete vote on question.
=======
    @token_required
    def delete(self, article_id):
        """
        Delete current user vote on question.
>>>>>>> dev

        :param article_id: The vote article ID.

        :return:
        """
        controller = VoteController()
        return controller.delete(article_id=article_id)
