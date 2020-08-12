#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.article.favorite.favorite_dto import FavoriteDto
from app.modules.article.favorite.favorite_controller import FavoriteController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = FavoriteDto.api
<<<<<<< HEAD
favorite_request = FavoriteDto.model_request
favorite_response = FavoriteDto.model_response


# @api.route('')
# class FavoriteList(Resource):
#     # @admin_token_required
#     # # @api.marshal_list_with(favorite)
#     # def get(self):
#     #     """
#     #     Get list of favorites from database.
#     #
#     #     :return: The list of comments.
#     #     """
#     #     controller = FavoriteController()
#     #     return controller.get()
#
#     @token_required
#     @api.expect(favorite_request)
#     @api.response(code=200, model=favorite_response, description='The model response for favorite.')
#     def post(self):
#         """
#         Create new favorite.
#
#         :return: The new comment if it was created successfully and null vice versa.
#         """
#         data = api.payload
#         controller = FavoriteController()
#         return controller.create(data=data)


# @api.route('/<int:id>')
class Favorite(Resource):
    @token_required
    @api.param(name='id', description='The favorite ID')
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def get(self, id):
        """
        Get favorite by its ID.

        :param comment_id: The ID of the comment.

        :return: The comment with the specific ID.
        """
        controller = FavoriteController()
        return controller.get_by_id(object_id=id)

    # @token_required
    # @api.expect(favorite_request)
    # @api.response(code=200, model=favorite_response, description='The model for favorite.')
    # def put(self, id):
    #     """
    #     Update existing comment by its ID.
    #
    #     :param comment_id: The ID of the comment which need to be updated.
    #
    #     :return: The updated comment if success and null vice versa.
    #     """
    #     data = api.payload
    #     controller = FavoriteController()
    #     return controller.update(object_id=id, data=data)

    # @token_required
    # def delete(self, id):
    #     """
    #     Delete comment by its ID.
    #
    #     :param comment_id: The ID of the comment.
    #
    #     :return:
    #     """
    #     controller = FavoriteController()
    #     return controller.delete(object_id=id)


@api.route('/user')
class FavoriteUser(Resource):
    @token_required
    @api.expect(favorite_request)
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def post(self):
        """
        Create a favorite on user.

        :param data: The data in dictionary form.

        :return: The favorite if success and null vice versa.
        """
        controller = FavoriteController()
        data = api.payload
        return controller.create_favorite_user(data=data)

    @token_required
    @api.param(name='id', description='The ID of the favorite to delete.')
    def delete(self, id):
        """
        Delete favorite on user.
=======
_favorite_request = FavoriteDto.model_request
_favorite_response = FavoriteDto.model_response
_vote_get_params = FavoriteDto.model_get_parser

@api.route('')
class FavoriteUser(Resource):
    @token_required
    @api.expect(_vote_get_params)
    def get(self, article_id):
        """
        Search all favorite that satisfy conditions.
        ---------------------
>>>>>>> dev

        :user_id: Search votes by user_id

<<<<<<< HEAD
        :return: True if success and False vice versa.
        """
        controller = FavoriteController()
        return controller.delete_favorite_user(object_id=id)
=======
        :article_id: Search all votes by article ID.
>>>>>>> dev

        :from_date: Search votes by from date.

        :to_date: Search votes by to date.

        :return: List of comments.
        """
        args = _vote_get_params.parse_args()
        controller = FavoriteController()
        return controller.get(article_id=article_id, args=args)

    @token_required
    @api.expect(_favorite_request)
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, article_id):
        '''
        Create a favorite on current user.

        :param article_id: The ID of the article to favorite.

        :param data: The data in dictionary form.

        :return: The favorite if success and null vice versa.
        '''
        controller = FavoriteController()
        data = api.payload
        return controller.create(article_id=article_id, data=data)

    @token_required
    def delete(self, article_id):
        '''
        Delete favorite on current user.

        :param article_id: The article ID of the favorite to delete.

        :return: True if success and False vice versa.
        '''
        controller = FavoriteController()
        return controller.delete(article_id=article_id)
