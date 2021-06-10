#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party module
from flask_restx import Namespace, fields

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionShareDto(Dto):
    name = 'question_share'
    api = Namespace(name, description="Question-Share operations")

    model_question = api.model('share_question',{
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite')
    })


    model_request = api.model('share_question_request', {
        'user_shared_to_id': fields.Integer(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Integer(description='')
    })

    model_response = api.model('share_question_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'user_shared_to_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'question': fields.Nested(model_question, description=''),
    })

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=False, help='Search shares by user_id')
    parser.add_argument('from_date', type=str, required=False, help='Search all shares by start date.')
    parser.add_argument('to_date', type=str, required=False, help='Search all shares by finish date.')
    parser.add_argument('facebook', type=str, required=False, help='Search all shares to Facebook.')
    parser.add_argument('twitter', type=str, required=False, help='Search all shares to Twitter.')
    parser.add_argument('zalo', type=str, required=False, help='Search all shares to Zalo.')
