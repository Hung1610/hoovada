#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.post.comment.comment_controller import CommentController
# own modules
# from common.decorator import token_required
from app.modules.post.comment.comment_dto import CommentDto
from common.utils.decorator import (admin_token_required, is_not_owner,
                                    token_required)

api = CommentDto.api
comment_response = CommentDto.model_response
comment_request = CommentDto.model_request

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search comments by user_id (who created answer)')
# parser.add_argument('question_id', type=str, required=False, help='Search all comments by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all comments by answer_id.')

@api.route('/<int:post_id>/comment')
class CommentList(Resource):
    # @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, post_id):
        """
        Search all comments that satisfy conditions.
        ---------------------

        :user_id: Search comments by user_id

        :post_id: Search all comments by post ID.

        :return: List of comments.
        """
        args = parser.parse_args()
        controller = CommentController()
        return controller.get(post_id=post_id, args=args)

    # @token_required
    @api.expect(comment_request)
    @is_not_owner(table_name='post', object_id_arg_name='post_id', creator_field_name='post_by_user')
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self, post_id):
        """
        Create new comment.

        :return: The new comment if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = CommentController()
        return controller.create(data=data, post_id=post_id)


@api.route('/all/comment/<int:id>')
class Comment(Resource):
    @token_required
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        """
        Get comment by its ID.

        :param id: The ID of the comment.

        :return: The comment with the specific ID.
        """
        controller = CommentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(comment_request)
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def put(self, id):
        """
        Update existing comment by its ID.

        :param id: The ID of the comment which need to be updated.

        :return: The updated comment if success and null vice versa.
        """
        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete comment by its ID.

        :param id: The ID of the comment.

        :return:
        """
        controller = CommentController()
        return controller.delete(object_id=id)
