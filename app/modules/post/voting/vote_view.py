#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.post.voting.vote_controller import VoteController
# own modules
from app.modules.post.voting.vote_dto import VoteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = VoteDto.api
_vote_request_post = VoteDto.model_request_post
_vote_response = VoteDto.model_response
_vote_get_params = VoteDto.model_get_parser
        

#@api.route('/<int:post_id>/vote')
class VotePost(Resource):
    @api.expect(_vote_get_params)
    def get(self, post_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = VoteController()
        return controller.get(post_id=post_id, args=args)

    @token_required
    @api.expect(_vote_request_post)
    @api.response(code=200, model=_vote_response, description='The model for vote response.')
    def post(self, post_id):
        """
        Create/Update current user vote on post.
        """

        controller = VoteController()
        data = api.payload
        return controller.create(post_id=post_id, data=data)

    @token_required
    def delete(self, post_id):
        """
        Delete current user vote on question.
        """
        
        controller = VoteController()
        return controller.delete(post_id=post_id)
