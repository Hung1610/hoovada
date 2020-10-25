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


class QuestionTopicDto(Dto):
    name = 'question_topic'
    api = Namespace(name, description="Question-Topic operations")

    model_request = api.model('question_topic_request', {
        'question_id': fields.Integer(required=True, description='The ID of the question'),
        'topic_id': fields.Integer(required=True, description='The ID of the topic')
    })
    model_response = api.model('question_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of question topic record'),
        'question_id': fields.Integer(required=True, description='The ID of the question'),
        'topic_id': fields.Integer(required=True, description='The ID of the topic'),
        'created_date':fields.DateTime(description='The date question_topic record was created')
    })
