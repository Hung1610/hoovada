#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.topic.report.report_controller import ReportController
from app.modules.topic.report.report_dto import TopicReportDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TopicReportDto.api
report_request = TopicReportDto.model_request
report_response = TopicReportDto.model_response
_get_parser = TopicReportDto.get_parser

@api.route('/<int:topic_id>/report')
class TopicReport(Resource):
    @token_required
    @api.expect(_get_parser)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, topic_id):
        """Get all reports that satisfy conditions."""

        args = _get_parser.parse_args()
        controller = ReportController()
        return controller.get(topic_id=topic_id, args=args)

    @token_required
    @api.expect(report_request)
    def post(self, topic_id):
        """Create topic report"""

        controller = ReportController()
        data = api.payload
        return controller.create(topic_id=topic_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @token_required
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):
        """Get report by its ID"""

        controller = ReportController()
        return controller.get_by_id(object_id=id)