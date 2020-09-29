#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.comment.voting.vote_dto import AnswerCommentVoteDto
from app.modules.q_a.answer.comment.voting.vote_controller import AnswerCommentVoteController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = AnswerCommentVoteDto.api
_vote_request_comment = AnswerCommentVoteDto.model_request_comment
_vote_response = AnswerCommentVoteDto.model_response
_vote_get_params = AnswerCommentVoteDto.model_get_parser
        

@api.route('/<int:comment_id>/vote')
class VoteComment(Resource):
    @api.expect(_vote_get_params)
    def get(self, comment_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = AnswerCommentVoteController()
        return controller.get(comment_id=comment_id, args=args)

    @token_required
    @api.expect(_vote_request_comment)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, comment_id):
        """
        Create/Update current user vote on comment.
        """

        controller = AnswerCommentVoteController()
        data = api.payload
        return controller.create(comment_id=comment_id, data=data)

    @token_required
    def delete(self, comment_id):
        """
        Delete current user vote on comment.
        """
        
        controller = AnswerCommentVoteController()
        return controller.delete(comment_id=comment_id)