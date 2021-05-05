#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.comment.comment_controller import CommentController
from app.modules.q_a.answer.comment.comment_dto import CommentDto
from common.utils.decorator import admin_token_required, token_required

api = CommentDto.api
comment_response = CommentDto.model_response
comment_request = CommentDto.model_request

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


parser = reqparse.RequestParser()
parser.add_argument('answer_id', type=str, required=False, help='Search all comments by answer_id.')


@api.route('/<int:answer_id>/comment')
class CommentList(Resource):
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, answer_id):
        """Get all comments by answer ID"""

        args = parser.parse_args()
        controller = CommentController()
        return controller.get(answer_id=answer_id, args=args)

    @api.expect(comment_request)
    @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self, answer_id):
        """Create new comment"""

        data = api.payload
        controller = CommentController()
        return controller.create(data=data, answer_id=answer_id)


@api.route('/all/comment/<int:id>')
class Comment(Resource):
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        """Get comment by its ID."""
        controller = CommentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(comment_request)
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def put(self, id):
        """Update existing comment by its ID"""
        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete comment by its ID"""
        controller = CommentController()
        return controller.delete(object_id=id)
