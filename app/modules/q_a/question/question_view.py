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
get_similar_questions_parser = QuestionDto.get_similar_questions_parser
question_invite_request = QuestionDto.question_invite_request
top_user_reputation_args_parser = QuestionDto.top_user_reputation_args_parser
top_user_reputation_response = QuestionDto.top_user_reputation_response
model_topic = QuestionDto.model_topic
get_relevant_topics_parser = QuestionDto.get_relevant_topics_parser
model_answer_request = QuestionDto.model_answer_request
model_question_proposal_response = QuestionDto.model_question_proposal_response
model_request = QuestionDto.model_question_request
model_response = QuestionDto.model_question_response

@api.route('')
class QuestionList(Resource):
    # @api.marshal_list_with(question)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """ 
        Get list of questions from database.
        """

        controller = QuestionController()
        return controller.get()


    # @token_required
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


@api.route('/recommended-users')
class QuestionRecommendedUsers(Resource):
    @api.expect(top_user_reputation_args_parser)
    @api.response(code=200, model=top_user_reputation_response, description='Model for top users response.')
    def get(self):
        """ 
        Get recommended users for question specifications.
        """
        args = top_user_reputation_args_parser.parse_args()
        controller = QuestionController()
        return controller.get_recommended_users(args=args)


@api.route('/recommended-topics')
class QuestionRecommendedTopics(Resource):
    @api.expect(get_relevant_topics_parser)
    @api.response(code=200, model=model_topic, description='Model for topic response.')
    def get(self):
        """ 
        Get recommended topics based on title.
        """
        args = get_relevant_topics_parser.parse_args()
        controller = QuestionController()
        return controller.get_recommended_topics(args=args)


@api.route('/similar')
class QuestionSimilar(Resource):
    @api.expect(get_similar_questions_parser)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """ 
        Get similar questions.
        """
        args = get_similar_questions_parser.parse_args()
        controller = QuestionController()
        return controller.get_similar(args=args)


@api.route('/<string:id_or_slug>')
class Question(Resource):
    # @api.marshal_with(question)
    # @api.param(name='id', description='The ID of thequestion.')
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self, id_or_slug):
        """ 
        Get specific question by its ID.
        """

        controller = QuestionController()
        return controller.get_by_id(object_id=id_or_slug)

    @admin_token_required
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

@api.route('/<string:id_or_slug>/answer')
class QuestionAnswer(Resource):
    # @token_required
    @api.expect(model_answer_request)
    def post(self, id_or_slug):
        """ 
        Create answer for question by its ID.
        """

        data = api.payload
        controller = QuestionController()
        return controller.create_answer(object_id=id_or_slug, data=data)

@api.route('/<string:id_or_slug>/invite')
class QuestionInvite(Resource):
    @token_required
    @api.expect(question_invite_request)
    def post(self, id_or_slug):
        """ 
        Delete the question by its ID.
        """

        data = api.payload
        controller = QuestionController()
        return controller.invite(object_id=id_or_slug, data=data)

proposal_get_parser = reqparse.RequestParser()
proposal_get_parser.add_argument('from_date', type=str, required=False, help='Search questions created later that this date.')
proposal_get_parser.add_argument('to_date', type=str, required=False, help='Search questions created before this data.')
@api.route('/<string:id_or_slug>/proposal')
class QuestionProposal(Resource):
    @api.expect(proposal_get_parser)
    @api.response(code=200, model=model_question_proposal_response, description='Model for question response.')
    def get(self, id_or_slug):
        """ 
        Get list of questions from database.
        """
        args = proposal_get_parser.parse_args()
        controller = QuestionController()
        return controller.get_proposals(object_id=id_or_slug, args=args)

    @token_required
    @api.expect(model_request)
    def post(self, id_or_slug):
        """ 
        Create question change proposal by its ID.
        """

        data = api.payload
        controller = QuestionController()
        return controller.create_proposal(object_id=id_or_slug, data=data)

@api.route('/all/proposal/<int:id>/approve')
class QuestionApprove(Resource):
    @admin_token_required
    @api.response(code=200, model=model_question_proposal_response, description='Model for question response.')
    def put(self, id):
        """ 
        Approve question change proposal
        """
        controller = QuestionController()
        return controller.approve_proposal(object_id=id)


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
