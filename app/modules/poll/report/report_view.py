#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.poll.report.report_controller import ReportController
from app.modules.poll.report.report_dto import ReportDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ReportDto.api
report_request = ReportDto.model_request
report_response = ReportDto.model_response
_get_parser = ReportDto.get_parser

@api.route('/<int:poll_id>/report')
class ReportUser(Resource):
    @token_required
    @api.expect(_get_parser)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, poll_id):
        """Search all report that satisfy conditions."""

        args = _get_parser.parse_args()
        controller = ReportController()
        return controller.get(poll_id=poll_id, args=args)

    @token_required
    @api.expect(report_request)
    def post(self, poll_id):
        """Create report"""

        controller = ReportController()
        data = api.payload
        return controller.create(poll_id=poll_id, data=data)


@api.route('/all/report/<int:id>')
class Reporting(Resource):
    @admin_token_required()
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):
        """Get report by report IO"""

        controller = ReportController()
        return controller.get_by_id(object_id=id)