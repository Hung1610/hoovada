#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class SearchDto(Dto):
    name = 'search'
    api = Namespace(name)

    model_search_question_res = api.model('search_question_res', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
    })

    model_search_topic_res = api.model('search_topic_res', {
        'id': fields.Integer(readonly=True, description=''),
        'name': fields.String(description='The name of the topic'),
    })

    model_search_user_res = api.model('search_user_res', {
        'id': fields.Integer(readonly=True, description=''),
        'email': fields.String(description='The email of the topic'),
        'display_name': fields.String(description='The display name of the topic')
    })

    search_response = api.model('response', {
        'message': fields.String(required=True)
    })