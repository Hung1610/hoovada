#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicReportDto(Dto):
    name = 'topic_report'
    api = Namespace(name, description="Topic report operations")

    model_request = api.model('topic_report_request', {
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description='')
    })

    model_response = api.model('topic_report_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'topic_id': fields.Integer(description=''),
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description=''),
        'created_date': fields.DateTime(description='')
    })

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('user_id', type=str, required=False, help='Search reports by user_id')
    get_parser.add_argument('topic_id', type=str, required=False, help='Search all reports by question_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search all reports by start created date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search all reports by finish created date.')

