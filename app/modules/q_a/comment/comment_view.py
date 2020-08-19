#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.comment.comment_dto import CommentDto
from app.modules.q_a.comment.comment_controller import CommentController
from app.modules.auth.decorator import admin_token_required, token_required

api = CommentDto.api
comment_response = CommentDto.model_response
comment_request = CommentDto.model_request

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('')
class CommentList(Resource):
    # @admin_token_required
    # # @api.marshal_list_with(comment)
    # def get(self):
    #     """
    #     Get list of comments from database.
    #
    #     :return: The list of comments.
    #     """
    #     controller = CommentController()
    #     return controller.get()

    @token_required
    @api.expect(comment_request)
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self):
        """
        Create new comment.
        """

        data = api.payload
        controller = CommentController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Comment(Resource):
    @token_required
    # @api.marshal_with(comment)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        """
        Get comment by its ID.
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
        """

        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete comment by its ID.
        """

        controller = CommentController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search comments by user_id (who created answer)')
# parser.add_argument('question_id', type=str, required=False, help='Search all comments by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all comments by answer_id.')


@api.route('/search')
@api.expect(parser)
class CommentSearch(Resource):
    @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self):
        """
        Search all comments that satisfy conditions.
        """
        
        args = parser.parse_args()
        controller = CommentController()
        return controller.search(args=args)
