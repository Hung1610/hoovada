#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.poll.comment.report.report_controller import ReportController
from app.modules.poll.comment.report.report_dto import PollCommentReportDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollCommentReportDto.api
report_request = PollCommentReportDto.model_request
report_response = PollCommentReportDto.model_response
_get_parser = PollCommentReportDto.get_parser

@api.route('/<int:comment_id>/report')
class PollCommentReport(Resource):
    @api.expect(_get_parser)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, comment_id):

        args = _get_parser.parse_args()
        controller = ReportController()
        return controller.get(comment_id=comment_id, args=args)

    @token_required
    @api.expect(report_request)
    def post(self, comment_id):

        controller = ReportController()
        data = api.payload
        return controller.create(comment_id=comment_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @admin_token_required()
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):


        controller = ReportController()
        return controller.get_by_id(object_id=id)