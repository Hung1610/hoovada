#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.voting.vote_dto import AnswerVoteDto
from app.modules.q_a.answer.voting.vote_controller import AnswerVoteController
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = AnswerVoteDto.api
_vote_request_answer = AnswerVoteDto.model_request_answer
_vote_response = AnswerVoteDto.model_response
_vote_get_params = AnswerVoteDto.model_get_parser
        

@api.route('/<int:answer_id>/vote')
class VoteAnswer(Resource):
    @api.expect(_vote_get_params)
    def get(self, answer_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = AnswerVoteController()
        return controller.get(answer_id=answer_id, args=args)

    @token_required
    @api.expect(_vote_request_answer)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, answer_id):
        """
        Create/Update current user vote on answer.
        """

        controller = AnswerVoteController()
        data = api.payload
        return controller.create(answer_id=answer_id, data=data)

    @token_required
    def delete(self, answer_id):
        """
        Delete current user vote on answer.
        """
        
        controller = AnswerVoteController()
        return controller.delete(answer_id=answer_id)
