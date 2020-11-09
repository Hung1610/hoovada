#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.q_a.answer.improvement.voting.vote_controller import AnswerImprovementVoteController
# own modules
from app.modules.q_a.answer.improvement.voting.vote_dto import AnswerImprovementVoteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerImprovementVoteDto.api
_vote_request = AnswerImprovementVoteDto.model_request_answer
_vote_response = AnswerImprovementVoteDto.model_response
_vote_get_params = AnswerImprovementVoteDto.model_get_parser
        

@api.route('/<int:improvement_id>/vote')
class VoteAnswerImprovement(Resource):
    @api.expect(_vote_get_params)
    def get(self, improvement_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        args['improvement_id'] = improvement_id
        controller = AnswerImprovementVoteController()
        return controller.get(args=args)

    @token_required
    @api.expect(_vote_request)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, improvement_id):
        """
        Create/Update current user vote on answer improvement.
        """

        controller = AnswerImprovementVoteController()
        data = api.payload
        return controller.create(improvement_id=improvement_id, data=data)

    @token_required
    def delete(self, improvement_id):
        """
        Delete current user vote on answer improvement.
        """
       
        controller = AnswerImprovementVoteController()
        return controller.delete(improvement_id=improvement_id)
