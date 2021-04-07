#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource

# own modules
from app.modules.q_a.question.question_controller import QuestionController
from app.modules.q_a.question.question_dto import QuestionDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionDto.api
get_parser = QuestionDto.get_parser
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
proposal_get_parser = QuestionDto.proposal_get_parser


@api.route('')
class QuestionList(Resource):

    @api.expect(get_parser)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """Get list of questions from params"""

        args = get_parser.parse_args()
        controller = QuestionController()
        return controller.get(args=args)

    @token_required
    @api.expect(model_request)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def post(self):
        """ Create new question"""

        data = api.payload
        controller = QuestionController()
        result = controller.create(data=data)
        return result


@api.route('/recommended-users')
class QuestionRecommendedUsers(Resource):
    @api.expect(top_user_reputation_args_parser)
    @api.response(code=200, model=top_user_reputation_response, description='Model for top users response.')
    def get(self):
        """ Get recommended users for question."""

        args = top_user_reputation_args_parser.parse_args()
        controller = QuestionController()
        return controller.get_recommended_users(args=args)


@api.route('/recommended-topics')
class QuestionRecommendedTopics(Resource):
    @api.expect(get_relevant_topics_parser)
    @api.response(code=200, model=model_topic, description='Model for topic response.')
    def get(self):
        """ Get recommended topics based on title."""

        args = get_relevant_topics_parser.parse_args()
        controller = QuestionController()
        return controller.get_recommended_topics(args=args)


@api.route('/similar')
class QuestionSimilar(Resource):
    @api.expect(get_similar_questions_parser)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def get(self):
        """ Get similar questions."""

        args = get_similar_questions_parser.parse_args()
        controller = QuestionController()
        return controller.get_similar(args=args)


def get_question_key_prefix():
    return '{}{}'.format('get.question', request.view_args['id_or_slug'])
    
@api.route('/<string:id_or_slug>')
class Question(Resource):
    @api.response(code=200, model=model_response, description='Model for question response.')
    @cache.cached(key_prefix=get_question_key_prefix)
    def get(self, id_or_slug):
        """ Get specific question by question Id or slug"""

        controller = QuestionController()
        return controller.get_by_id(object_id=id_or_slug)

    @admin_token_required()
    @api.expect(model_request)
    @api.response(code=200, model=model_response, description='Model for question response.')
    def put(self, id_or_slug):
        """ Update existing question by question Id or slug.  NOTE: topic_ids does not be supported in update API. Please send question update format without topic_ids."""

        data = api.payload
        controller = QuestionController()
        result = controller.update(object_id=id_or_slug, data=data)
        cache.clear_cache(get_question_key_prefix())
        return result

    @admin_token_required()
    def delete(self, id_or_slug):
        """ Delete the question by question Id or slug"""

        controller = QuestionController()
        result = controller.delete(object_id=id_or_slug)
        cache.clear_cache(get_question_key_prefix())
        return result

@api.route('/<string:id_or_slug>/invite')
class QuestionInvite(Resource):
    @token_required
    @api.expect(question_invite_request)
    def post(self, id_or_slug):
        """Create invited question by question Id or slug"""

        data = api.payload
        controller = QuestionController()
        return controller.invite(object_id=id_or_slug, data=data)

@api.route('/<string:id_or_slug>/decline-invite')
class QuestionDeclineInvite(Resource):
    @token_required
    @api.expect(question_invite_request)
    def post(self, id_or_slug):
        """Create invited question by question Id or slug"""
        controller = QuestionController()
        return controller.decline_invited_question(object_id=id_or_slug)

@api.route('/<string:id_or_slug>/friend-invite')
class QuestionFriendInvite(Resource):
    @token_required
    def post(self, id_or_slug):
        """Create the invited question to all friends by question Id or slug"""

        controller = QuestionController()
        return controller.invite_friends(object_id=id_or_slug)


def get_question_proposal_key_prefix():
    return '{}{}'.format('get.question.proposals', request.view_args['id_or_slug'])

@api.route('/<string:id_or_slug>/proposal')
class QuestionProposal(Resource):
    @api.expect(proposal_get_parser)
    @api.response(code=200, model=model_question_proposal_response, description='Model for question response.')
    @cache.cached(key_prefix=get_question_proposal_key_prefix)
    def get(self, id_or_slug):
        """ Get list of questions proposal by question Id or slug"""

        args = proposal_get_parser.parse_args()
        controller = QuestionController()
        return controller.get_proposals(object_id=id_or_slug, args=args)

    @token_required
    @api.expect(model_request)
    def post(self, id_or_slug):
        """ Create question proposal by question Id or slug"""

        data = api.payload
        controller = QuestionController()
        result = controller.create_proposal(object_id=id_or_slug, data=data)
        cache.clear_cache(get_question_proposal_key_prefix())
        return result

@api.route('/<string:id_or_slug>/delete-proposal')
class QuestionDeleteProposal(Resource):
    @token_required
    def post(self, id_or_slug):
        """ Create question delete proposal by question Id or slug"""

        controller = QuestionController()
        result = controller.create_delete_proposal(object_id=id_or_slug)
        cache.clear_cache(get_question_proposal_key_prefix())
        return result


@api.route('/all/proposal/<int:id>/approve')
class QuestionApprove(Resource):
    @admin_token_required()
    @api.response(code=200, model=model_question_proposal_response, description='Model for question response.')
    def put(self, id):
        """Approve question change proposal"""

        controller = QuestionController()
        return controller.approve_proposal(object_id=id)

@api.route('/update_slug')
class UpdateSlug(Resource):
    @admin_token_required()
    @api.response(code=200, model=model_response, description='Model for question response.')
    def post(self):
        """ Update Slug using question Id or slug"""

        controller = QuestionController()
        controller.update_slug()
