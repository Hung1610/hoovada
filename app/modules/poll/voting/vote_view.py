#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.poll.voting.vote_controller import PollVoteController
# own modules
from app.modules.poll.voting.vote_dto import PollVoteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = PollVoteDto.api
_vote_request_poll = PollVoteDto.model_request_poll
_vote_response = PollVoteDto.model_response
_vote_get_params = PollVoteDto.model_get_parser
        

@api.route('/<int:poll_id>/vote')
class VoteAnswer(Resource):
    @api.expect(_vote_get_params)
    def get(self, poll_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = PollVoteController()
        return controller.get(poll_id=poll_id, args=args)

    @token_required
    @api.expect(_vote_request_poll)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, poll_id):
        """
        Create/Update current user vote on poll.
        """

        controller = PollVoteController()
        data = api.payload
        return controller.create(poll_id=poll_id, data=data)

    @token_required
    def delete(self, poll_id):
        """
        Delete current user vote on poll.
        """
        
        controller = PollVoteController()
        return controller.delete(poll_id=poll_id)
