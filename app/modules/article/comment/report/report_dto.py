#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleCommentReportDto(Dto):
    name = 'article_comment_report'
    api = Namespace(name, description="Article comment report operations")

    model_request = api.model('article_comment_report_request', {
        'report_type': fields.Integer(description='1 - General, 2 - Inapproriate, 3 - Duplicate', default=False),
        'description': fields.String(description='')
    })

    model_response = api.model('article_comment_report_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'report_type': fields.Integer(description='1 - General, 2 - Inapproriate, 3 - Duplicate', default=False),
        'description': fields.String(description=''),
        'created_date': fields.DateTime(description='')
    })

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('user_id', type=str, required=False, help='Search reports by user_id')
    get_parser.add_argument('comment_id', type=str, required=False, help='Search all reports by article_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search all reports by start created date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search all reports by finish created date.')

