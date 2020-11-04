#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.q_a.question.voting.vote_controller import \
    QuestionVoteController
# own modules
from app.modules.q_a.question.voting.vote_dto import QuestionVoteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = QuestionVoteDto.api
_vote_request_question = QuestionVoteDto.model_request_question
_vote_response = QuestionVoteDto.model_response
_vote_get_params = QuestionVoteDto.model_get_parser
        

@api.route('/<int:question_id>/vote')
class VoteQuestion(Resource):
    @api.expect(_vote_get_params)
    def get(self, question_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = QuestionVoteController()
        return controller.get(question_id=question_id, args=args)

    @token_required
    @api.expect(_vote_request_question)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, question_id):
        """
        Create/Update current user vote on question.
        """

        controller = QuestionVoteController()
        data = api.payload
        return controller.create(question_id=question_id, data=data)

    @token_required
    def delete(self, question_id):
        """
        Delete current user vote on question.
        """
        
        controller = QuestionVoteController()
        return controller.delete(question_id=question_id)
