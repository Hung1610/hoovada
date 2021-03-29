#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.post.post_controller import PostController
from app.modules.post.post_dto import PostDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PostDto.api
_post_dto_request = PostDto.model_post_request
_post_dto_response = PostDto.model_post_response
_post_get_params = PostDto.model_get_parser

@api.route('')
class PostList(Resource):
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    @api.expect(_post_get_params)
    #@cache.cached(query_string=True)
    def get(self):
        """Get all posts that satisfy param queries"""

        args = _post_get_params.parse_args()
        controller = PostController()
        return controller.get(args=args)


    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def post(self):
        """Create new post"""

        data = api.payload
        controller = PostController()
        return controller.create(data=data)


def get_post_proposal_key_prefix():
    return '{}{}'.format('get.post.proposals', request.view_args['post_id'])


@api.route('/<string:post_id>')
class Post(Resource):
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    @cache.cached(key_prefix=get_post_proposal_key_prefix)
    def get(self, post_id):
        """Get specific post by post Id"""

        controller = PostController()
        return controller.get_by_id(object_id=post_id)

    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def put(self, post_id):
        """Update existing post by post Id"""

        data = api.payload
        controller = PostController()
        result = controller.update(object_id=post_id, data=data, is_put=True)
        cache.clear_cache(get_post_proposal_key_prefix())
        return result

    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def patch(self, post_id):
        """Update existing post by post Id"""

        data = api.payload
        controller = PostController()
        result = controller.update(object_id=post_id, data=data)
        cache.clear_cache(get_post_proposal_key_prefix())
        return result

    @token_required
    def delete(self, post_id):
        """Delete the post by post id"""

        controller = PostController()
        result = controller.delete(object_id=post_id)
        cache.clear_cache(get_post_proposal_key_prefix())
        return result


parser_post_of_friend = reqparse.RequestParser()
parser_post_of_friend.add_argument('page', type=int, required=False, help='Search posts by page.')
parser_post_of_friend.add_argument('per_page', type=int, required=False, help='Get record number on page.')

@api.route('/post_of_friend')
@api.expect(parser_post_of_friend)
class PostOfFriend(Resource):
    @token_required
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def get(self):

        args = parser_post_of_friend.parse_args()
        controller = PostController()
        return controller.get_post_of_friend(args)
