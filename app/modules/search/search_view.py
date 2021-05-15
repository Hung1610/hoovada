#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.search.search_controller import SearchController
# own modules
from app.modules.search.search_dto import SearchDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = SearchDto.api
search_response = SearchDto.search_response

parser = reqparse.RequestParser()
parser.add_argument('value', type=str, required=False, help='The value of the search')

@api.route('/event_search')
@api.expect(parser)
class Search(Resource):
    @api.response(code=200, model=search_response, description='Model for success response.')
    def get(self):
        """ 
        Get search results satisfy conditions.
        """

        args = parser.parse_args()
        controller = SearchController()
        return controller.search_elastic(args=args)

@api.route('/article')
class ArticleSearch(Resource):
    @api.expect(SearchDto.search_model_request_parser)
    @api.response(code=200, model=SearchDto.model_search_article_res, description='Model for article response.')
    def get(self):
        """ Search articles by title"""

        args = SearchDto.search_model_request_parser.parse_args()
        controller = SearchController()
        return controller.search_article_by_title(args=args)

@api.route('/user')
class UserSearch(Resource):
    @api.expect(SearchDto.search_model_request_parser)
    @api.response(code=200, model=SearchDto.model_search_user_response, description='Model for user response.')
    def get(self):
        """ Search users by display name or email"""

        args = SearchDto.search_model_request_parser.parse_args()
        controller = SearchController()
        return controller.search_user_by_name_or_email(args=args)

@api.route('/poll')
class PollSearch(Resource):
    @api.expect(SearchDto.search_model_request_parser)
    @api.response(code=200, model=SearchDto.model_search_poll_response, description='Model for poll response.')
    def get(self):
        """ Search poll by title"""

        args = SearchDto.search_model_request_parser.parse_args()
        controller = SearchController()
        return controller.search_poll_by_title(args=args)

@api.route('/question')
class QuestionSearch(Resource):
    @api.expect(SearchDto.search_model_request_parser)
    @api.response(code=200, model=SearchDto.model_search_question_response, description='Model for question response.')
    def get(self):
        """ Search questions by title"""

        args = SearchDto.search_model_request_parser.parse_args()
        controller = SearchController()
        return controller.search_question_by_title(args=args)

@api.route('/topic')
class TopicSearch(Resource):
    @api.expect(SearchDto.search_model_request_parser)
    @api.response(code=200, model=SearchDto.model_search_topic_response, description='Model for topic response.')
    def get(self):
        """ Search topics by name"""

        args = SearchDto.search_model_request_parser.parse_args()
        controller = SearchController()
        return controller.search_topic_by_name(args=args)

@api.route('/user/<string:user_id>/friend')
class UserSearch(Resource):
    @api.expect(SearchDto.search_user_request_parser)
    @api.response(code=200, model=SearchDto.model_search_user_friend_response, description='Model for topic response.')
    def get(self, user_id):
        """ Search topics by name"""

        args = SearchDto.search_user_request_parser.parse_args()
        controller = SearchController()
        return controller.search_friend_by_name_or_email(args=args, user_id=user_id)