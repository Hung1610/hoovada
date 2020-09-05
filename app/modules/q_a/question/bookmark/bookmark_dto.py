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


class QuestionBookmarkDto(Dto):
    name = 'question_bookmark'
    api = Namespace(name, description="Question bookmark operations")

    model_topic_question_bookmark = api.model('topic_question_bookmark', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_bookmark_question = api.model('bookmark_question', {
        'title': fields.String(description='The title of the question'),
        'user_id': fields.Integer(description='The user information'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'topics': fields.List(fields.Nested(model_topic_question_bookmark), description='The list of topics')
    })

    model_request = api.model('bookmark_question_request', {
    })

    model_response = api.model('bookmark_question_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who bookmarkd'),
        'question_id': fields.Integer(required=False, description='The user ID who has been bookmarkd'),
        'question':fields.Nested(model_bookmark_question, description='The information of the question'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search bookmarks by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all bookmarks by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all bookmarks by finish voting date.')
    model_get_parser.add_argument('bookmarkd_user_id', type=str, required=False, help='Search bookmarks by user owner of the question')
