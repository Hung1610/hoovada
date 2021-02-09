#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.post.post_controller import PostController
from app.modules.post.post_dto import PostDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PostDto.api
_post_dto_request = PostDto.model_post_request
_post_dto_response = PostDto.model_post_response
_post_get_params = PostDto.model_get_parser
_post_get_similar_params = PostDto.get_similar_posts_parser

@api.route('')
class PostList(Resource):
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    @api.expect(_post_get_params)
    @cache.cached(query_string=True)
    def get(self):
        """
        Get all posts that satisfy conditions
        """

        args = _post_get_params.parse_args()
        controller = PostController()
        return controller.get(args=args)


    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def post(self):
        """
        Create new post and save to database.
        """

        data = api.payload
        controller = PostController()
        return controller.create(data=data)


@api.route('/<string:id_or_slug>')
class Post(Resource):
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def get(self, id_or_slug):
        """
        Get specific post by its ID.
        """

        controller = PostController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def put(self, id_or_slug):
        """
        Update existing post by its ID.
        """

        data = api.payload
        controller = PostController()
        return controller.update(object_id=id_or_slug, data=data, is_put=True)

    @token_required
    @api.expect(_post_dto_request)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def patch(self, id_or_slug):
        """
        Update existing post by its ID.
        """

        data = api.payload
        controller = PostController()
        return controller.update(object_id=id_or_slug, data=data)

    @admin_token_required()
    def delete(self, id_or_slug):
        """
        Delete the post by its ID.
        """

        controller = PostController()
        return controller.delete(object_id=id_or_slug)

        
@api.route('/similar')
class PostSimilar(Resource):
    @api.expect(_post_get_similar_params)
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def get(self):
        """ 
        Get similar posts.
        """
        args = _post_get_similar_params.parse_args()
        controller = PostController()
        return controller.get_similar(args=args)


@api.route('/update_slug')
class UpdatePostSlug(Resource):
    @admin_token_required()
    @api.response(code=200, model=_post_dto_response, description='Model for question response.')
    def post(self):
        """ 
        Update Slug for posts in DB
        """

        controller = PostController()
        return controller.update_slug()

parser_post_of_friend = reqparse.RequestParser()
parser_post_of_friend.add_argument('page', type=int, required=False, help='Search posts by page.')
parser_post_of_friend.add_argument('per_page', type=int, required=False, help='Get record number on page.')

@api.route('/post_of_friend')
@api.expect(parser_post_of_friend)
class PostOfFriend(Resource):
    @token_required
    @api.response(code=200, model=_post_dto_response, description='Model for post response.')
    def get(self):
        """ Lay danh sach post of freind and of follow
        """

        args = parser_post_of_friend.parse_args()
        controller = PostController()
        return controller.get_post_of_friend(args)
