#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.q_a.question.report.report_controller import ReportController
from app.modules.q_a.question.report.report_dto import QuestionReportDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionReportDto.api
REPORT_RESPONSE = QuestionReportDto.model_response
REPORT_REQUEST = QuestionReportDto.model_request
GET_PARSER = QuestionReportDto.get_parser


@api.route('/<int:question_id>/report')
class QuestionReport(Resource):
    @token_required
    @api.expect(GET_PARSER)
    @api.response(code=200, model=REPORT_RESPONSE, description='The model for report response.')
    def get(self, question_id):
        """Search all votes that satisfy conditions"""

        args = GET_PARSER.parse_args()
        controller = ReportController()
        return controller.get(question_id=question_id, args=args)

    @token_required
    @api.expect(REPORT_REQUEST)
    def post(self, question_id):
        """Create question report"""

        controller = ReportController()
        data = api.payload
        return controller.create(question_id=question_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @admin_token_required()
    @api.response(code=200, model=REPORT_RESPONSE, description='The model for report response.')
    def get(self, id):
        """Get report by its ID"""

        controller = ReportController()
        return controller.get_by_id(object_id=id)