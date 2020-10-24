#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.common.decorator import token_required
from app.modules.topic.question_topic.question_topic_dto import QuestionTopicDto
from app.modules.topic.question_topic.question_topic_controller import QuestionTopicController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionTopicDto.api
question_topic_request = QuestionTopicDto.model_request
question_topic_response = QuestionTopicDto.model_response


@api.route('')
class QuestionTopicList(Resource):
    @admin_token_required()
    @api.response(code=200, model=question_topic_response, description='Model for question topic response.')
    def get(self):
        """
        Get list of question_topics from database.

        :return: The list of question_topics.
        """
        controller = QuestionTopicController()
        return controller.get()

    @admin_token_required()
    @api.expect(question_topic_request)
    # @api.marshal_with(question_topic)
    @api.response(code=200, model=question_topic_response, description='Model for question topic response.')
    def post(self):
        """
        Create new question_topic.
        """

        data = api.payload
        controller = QuestionTopicController()
        return controller.create(data=data)


@api.route('/<int:id>')
class QuestionTopic(Resource):
    @token_required
    # @api.marshal_with(question_topic)
    @api.response(code=200, model=question_topic_response, description='Model for question topic response.')
    def get(self, id):
        """
        Get question_topic by its ID.
        """

        controller = QuestionTopicController()
        return controller.get_by_id(object_id=id)

    # @token_required
    # @api.expect(question_topic)
    # # @api.marshal_with(question_topic)
    # def put(self, id):
    #     """
    #     Update existing question_topic by its ID.
    #
    #     :param id: The ID of the question_topic which need to be updated.
    #
    #     :return: The updated question_topic if success and null vice versa.
    #     """
    #     data = api.payload
    #     controller = QuestionTopicController()
    #     return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete question_topic by its ID.
        """

        controller = QuestionTopicController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('question_id', type=str, required=False, help='The question ID.')
parser.add_argument('topic_id', type=str, required=False, help='The topic ID.')


@api.route('/search')
@api.expect(parser)
class QuestionTopicSearch(Resource):
    @token_required
    @api.response(code=200, model=question_topic_response, description='Model for question topic response.')
    def get(self):
        """
        Search all question-topics that satisfy conditions.
        """

        args = parser.parse_args()
        controller = QuestionTopicController()
        return controller.search(args=args)


@api.route('/delete')
@api.expect(parser)
class QuestionTopicDelete(Resource):
    @admin_token_required()
    def delete(self):
        """
        Delete question_topic by question_id and topic_id
        """
        
        args = parser.parse_args()
        controller = QuestionTopicController()
        return controller.delete_by_question_id_topic_id(args)
