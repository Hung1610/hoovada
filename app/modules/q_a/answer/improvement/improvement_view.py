#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.improvement.improvement_controller import AnswerImprovementController
from app.modules.q_a.answer.improvement.improvement_dto import AnswerImprovementDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerImprovementDto.api
improvement_request = AnswerImprovementDto.model_request
improvement_response = AnswerImprovementDto.model_response
get_parser = AnswerImprovementDto.get_parser
        

@api.route('/<int:answer_id>/improvement')
class AnswerImprovementList(Resource):
    @api.expect(get_parser)
    def get(self, answer_id):
        """
        Search all improvements that satisfy conditions.
        """

        args = get_parser.parse_args()
        args['answer_id'] = answer_id
        controller = AnswerImprovementController()
        return controller.get(args=args)

    @token_required
    @api.expect(improvement_request)
    @api.response(code=200, model=improvement_response, description='The model for improvement response.')
    def post(self, answer_id):
        """
        Create/Update current user improvement on answer.
        """

        controller = AnswerImprovementController()
        data = api.payload
        return controller.create(answer_id=answer_id, data=data)


@api.route('/all/improvement')
class AnswerImprovementAllList(Resource):
    @api.expect(get_parser)
    @api.response(code=200, model=improvement_response, description='Model for answer response.')
    @cache.cached(query_string=True)
    def get(self):
        """
        Get the list of answers from database.

        :return: List of answers.
        """
        args = get_parser.parse_args()
        controller = AnswerImprovementController()
        return controller.get(args=args)


@api.route('/all/improvement/<int:id>')
class AnswerImprovement(Resource):
    @token_required
    # @api.marshal_with(answer)
    @api.response(code=200, model=improvement_response, description='Model for answer response.')
    def get(self, id):
        """
        Get the answer by its ID.
        """

        controller = AnswerImprovementController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(improvement_request)
    # @api.marshal_with(answer)
    @api.response(code=200, model=improvement_response, description='Model for answer response.')
    def put(self, id):
        """
        Update the existing answer by its ID.
        """

        data = api.payload
        controller = AnswerImprovementController()
        return controller.update(object_id=id, data=data)

    @admin_token_required()
    def delete(self, id):
        """
        Delete existing answer by its ID.
        """

        controller = AnswerImprovementController()
        return controller.delete(object_id=id)
