#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.question.comment.report.report_dto import QuestionCommentReportDto
from app.modules.q_a.question.comment.report.report_controller import ReportController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = QuestionCommentReportDto.api
report_request = QuestionCommentReportDto.model_request
report_response = QuestionCommentReportDto.model_response
_get_parser = QuestionCommentReportDto.get_parser

@api.route('/<int:comment_id>/report')
class QuestionCommentReport(Resource):
    @token_required
    @api.expect(_get_parser)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, comment_id):
        """
        Search all votes that satisfy conditions.
        """

        args = _get_parser.parse_args()
        controller = ReportController()
        return controller.get(comment_id=comment_id, args=args)

    @token_required
    @api.expect(report_request)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def post(self, comment_id):
        """
        Make report
        """

        controller = ReportController()
        data = api.payload
        return controller.create(comment_id=comment_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @admin_token_required
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):
        """
        Get report by its ID.
        """

        controller = ReportController()
        return controller.get_by_id(object_id=id)