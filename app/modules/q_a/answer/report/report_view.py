#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.q_a.answer.report.report_controller import ReportController
from app.modules.q_a.answer.report.report_dto import AnswerReportDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerReportDto.api
report_request = AnswerReportDto.model_request
report_response = AnswerReportDto.model_response
_get_parser = AnswerReportDto.get_parser

@api.route('/<int:answer_id>/report')
class AnswerReport(Resource):
    @token_required
    @api.expect(_get_parser)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, answer_id):
        """Search all votes that satisfy conditions."""

        args = _get_parser.parse_args()
        controller = ReportController()
        return controller.get(answer_id=answer_id, args=args)

    @token_required
    @api.expect(report_request)
    def post(self, answer_id):
        """Create answer report"""

        controller = ReportController()
        data = api.payload
        return controller.create(answer_id=answer_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @admin_token_required()
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):
        """Get report by its ID"""

        controller = ReportController()
        return controller.get_by_id(object_id=id)