#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.question.comment.comment_controller import CommentController
from app.modules.q_a.question.comment.comment_dto import CommentDto
from common.utils.decorator import token_required

api = CommentDto.api
comment_response = CommentDto.model_response
comment_request = CommentDto.model_request

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


parser = reqparse.RequestParser()
parser.add_argument('question_id', type=str, required=False, help='Search all comments by question_id.')


@api.route('/<int:question_id>/comment')
class CommentList(Resource):
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, question_id):
        """ Get all comments by question ID"""

        args = parser.parse_args()
        controller = CommentController()
        return controller.get(question_id=question_id, args=args)

    @token_required
    @api.expect(comment_request)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self, question_id):
        """Create new comment"""
        data = api.payload
        controller = CommentController()
        return controller.create(data=data, question_id=question_id)


@api.route('/all/comment/<int:id>')
class Comment(Resource):
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        """Get comment by its comment ID."""

        controller = CommentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(comment_request)
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def patch(self, id):
        """Update existing comment by its ID."""

        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete comment by its ID"""

        controller = CommentController()
        return controller.delete(object_id=id)
