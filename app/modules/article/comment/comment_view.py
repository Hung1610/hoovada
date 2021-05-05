#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.article.comment.comment_controller import CommentController
# own modules
# from common.decorator import token_required
from app.modules.article.comment.comment_dto import CommentDto
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
parser.add_argument('article_id', type=str, required=False, help='Search comments by article_id')

@api.route('/<int:article_id>/comment')
class CommentList(Resource):
    # @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, article_id):
        """Get all comments by article ID"""

        args = parser.parse_args()
        controller = CommentController()
        return controller.get(article_id=article_id, args=args)

    @token_required
    @api.expect(comment_request)
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def post(self, article_id):
        """Create new comment"""

        data = api.payload
        controller = CommentController()
        return controller.create(data=data, article_id=article_id)


@api.route('/all/comment/<int:id>')
class Comment(Resource):
    @token_required
    @api.response(code=200, model=comment_response, description='Model for comment response.')
    def get(self, id):
        """Get comment by its ID"""
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
