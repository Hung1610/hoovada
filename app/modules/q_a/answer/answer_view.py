#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.answer.answer_controller import AnswerController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerDto.api
answer_upload_parser = AnswerDto.upload_parser
answer_request = AnswerDto.model_request
answer_response = AnswerDto.model_response

@api.route('/<int:id>/file')
@api.doc(params={'id': 'The answer ID'})
class AnswerFile(Resource):
    @token_required
    @api.expect(answer_upload_parser)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def post(self, id):
        """
        Create new answer with files (video/audio).
        """
        controller = AnswerController()
        return controller.create_with_file(object_id=id)

@api.route('')
class AnswerList(Resource):
    # @admin_token_required
    # # @api.marshal_list_with(answer)
    # @api.response(code=200, model=answer_response, description='Model for answer response.')
    # def get(self):
    #     """
    #     Get the list of answers from database.
    #
    #     :return: List of answers.
    #     """
    #     controller = AnswerController()
    #     return controller.get()

    @token_required
    @api.expect(answer_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def post(self):
        """
        Create new answer.
        """

        data = api.payload
        controller = AnswerController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Answer(Resource):
    @token_required
    # @api.marshal_with(answer)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def get(self, id):
        """
        Get the answer by its ID.
        """

        controller = AnswerController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(answer_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def put(self, id):
        """
        Update the existing answer by its ID.
        """

        data = api.payload
        controller = AnswerController()
        return controller.update(object_id=id, data=data)

    @admin_token_required
    def delete(self, id):
        """
        Delete existing answer by its ID.
        """

        controller = AnswerController()
        return controller.delete(object_id=id)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
parser.add_argument('question_id', type=str, required=False, help='Search all answers by question_id.')
# parser.add_argument('created_date', type=str, required=False, help='Search answers by created-date.')
# parser.add_argument('updated_date', type=str, required=False, help='Search answers by updated-date.')
parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')


@api.route('/search')
@api.expect(parser)
class AnswerSearch(Resource):
    @token_required
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def get(self):
        """
        Search all answers that satisfy conditions.
        """

        args = parser.parse_args()
        controller = AnswerController()
        return controller.search(args=args)
