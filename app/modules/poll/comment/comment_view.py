#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own module
from app.modules.poll.comment.comment_controller import CommentController
from app.modules.poll.comment.comment_dto import CommentDto
from common.utils.decorator import admin_token_required, is_not_owner, token_required

api = CommentDto.api
comment_response = CommentDto.model_response
comment_request = CommentDto.model_request

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search comments by user_id ')

@api.route('/<int:poll_id>/comment')
class CommentList(Resource):
    # @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, poll_id):
        args = parser.parse_args()
        controller = CommentController()
        return controller.get(poll_id=poll_id, args=args)

    @token_required
    @api.expect(comment_request)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self, poll_id):
        data = api.payload
        controller = CommentController()
        return controller.create(data=data, poll_id=poll_id)


@api.route('/all/comment/<int:id>')
class Comment(Resource):
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        controller = CommentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(comment_request)
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def put(self, id):
        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        controller = CommentController()
        return controller.delete(object_id=id)