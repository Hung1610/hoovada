#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportDto(Dto):
    name = 'report'
    api = Namespace(name)
    model_request = api.model('report_quest', {
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description='')
    })

    model_response = api.model('report_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description=''),
        'created_date': fields.DateTime(description='')
    })
