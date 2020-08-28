#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.question.question_dto import QuestionDto
from app.modules.q_a.question.question_controller import QuestionController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionDto.api
model_request = QuestionDto.model_question_request
model_response = QuestionDto.model_question_response

@api.route('')
class QuestionList(Resource):
    @token_required
    # @api.marshal_list_with(question)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """ 
        Get list of questions from database.
        """

        controller = QuestionController()
        return controller.get()


    @token_required
    @api.expect(model_request)
    # @api.marshal_with(question)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def post(self):
        """ 
        Create new question and save to database.
        """

        data = api.payload
        controller = QuestionController()
        return controller.create(data=data)


@api.route('/<string:id_or_slug>')
class Question(Resource):
    @token_required
    # @api.marshal_with(question)
    # @api.param(name='id', description='The ID of thequestion.')
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self, id_or_slug):
        """ 
        Get specific question by its ID.
        """

        controller = QuestionController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(model_request)
    # @api.marshal_with(question)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def put(self, id_or_slug):
        """ 
        Update existing question by its ID.  NOTE: topic_ids does not be supported in update API. Please send question update format without topic_ids.
        """

        data = api.payload
        controller = QuestionController()
        return controller.update(object_id=id_or_slug, data=data)

    @token_required
    def delete(self, id_or_slug):
        """ 
        Delete the question by its ID.
        """

        controller = QuestionController()
        return controller.delete(object_id=id_or_slug)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=False, help='Search question by its title')
parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
parser.add_argument('fixed_topic_id', type=str, required=False, help='Search all questions related to fixed-topic.')
parser.add_argument('topic_id', type=str, required=False, help='Search all questions related to topic.')
parser.add_argument('from_date', type=str, required=False, help='Search questions created later that this date.')
parser.add_argument('to_date', type=str, required=False, help='Search questions created before this data.')
parser.add_argument('anonymous', type=str, required=False, help='Search questions created by Anonymous.')


@api.route('/search')
@api.expect(parser)
class QuesstionSearch(Resource):
    @token_required
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """ 
        Search all questions that satisfy conditions.
        """

        args = parser.parse_args()
        controller = QuestionController()
        return controller.search(args=args)


@api.route('/get_by_slug/<string:slug>')
class GetQuestionBySlug(Resource):
    @token_required
    # @api.marshal_with(question)
    # @api.param(name='id', description='The ID of thequestion.')
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self, slug):
        """ 
        Get specific question by its ID.
        """

        controller = QuestionController()
        return controller.get_by_slug(slug)

@api.route('/update_slug')
class UpdateSlug(Resource):
    # @admin_token_required
    @api.response(code=200, model=model_response, description='Model for question response.')
    def post(self):
        """ 
        Update Slug for questions in DB
        """

        controller = QuestionController()
        return controller.update_slug()

# @api.route('/get_by_topic/<int:topic_id>')
# class GetQuestionByTopic(Resource):
#     # @token_required
#     @api.response(code=200, model=model_response, description='Model for question response.')
#     #13/07/2020 thongnv - add param `topic_id`
#     def get(self,topic_id):
#         """  Get all question of a topic that sorted based in upvote count.

#         Args:
#             `topic_id` (int): Search all questions by topic ID.

#         Returns:
#              Get all question of a topic that sorted based in upvote count.
#         """

#         controller = QuestionController()
#         return controller.get_by_topic_id(topic_id)
