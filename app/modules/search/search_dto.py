#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class SearchDto(Dto):
    name = 'search'
    api = Namespace(name, description="Search operations")

    model_search_question_res = api.model('search_question_res', {
        'id': fields.Integer(readonly=True, description=''),
        'slug': fields.String(description='The slug of the question'),
        'title': fields.String(description='The title of the question'),
    })

    model_search_topic_res = api.model('search_topic_res', {
        'id': fields.Integer(readonly=True, description=''),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
    })

    model_search_user_res = api.model('search_user_res', {
        'id': fields.Integer(readonly=True, description=''),
        'email': fields.String(description='The email of the topic'),
        'display_name': fields.String(description='The display name of the topic')
    })

    model_search_article_res = api.model('search_article_res', {
        'id': fields.Integer(readonly=True, description=''),
        'slug': fields.String(description='The slug of the article'),
        'title': fields.String(description='The title of the article'),
    })

    search_response = api.model('response', {
        'message': fields.String(required=True)
    })