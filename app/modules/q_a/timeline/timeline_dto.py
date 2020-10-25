#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto
from app.modules.q_a.timeline.timeline import Timeline, TimelineActivity

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class TimelineDto(Dto):
    name = 'timeline'
    api = Namespace(name, description="Question-Timeline operations")

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search timeline by user id')
    model_get_parser.add_argument('question_id', type=int, required=False, help='Search all timelines related to question id.')
    model_get_parser.add_argument('answer_id', type=int, required=False, help='Search all timelines related to answer id.')
    model_get_parser.add_argument('comment_id', type=int, required=False, help='Search all timelines related to comment id.')
    model_get_parser.add_argument('article_id', type=int, required=False, help='Search all timelines related to article id.')
    model_get_parser.add_argument('article_comment_id', type=int, required=False, help='Search all timelines related to article comment id.')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search timelines created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search timelines created before this data.')
    
    model_timeline_user = api.model(name + '_' + 'user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    timeline_model_request = api.model(name + '_' + 'model_request', {
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'question_comment_id': fields.Integer(default=0, description='The ID of the question comment'),
        'answer_id': fields.Integer(default=0, description='The ID of the answer'),
        'answer_comment_id': fields.Integer(default=0, description='The ID of the answer comment'),
        'article_id': fields.Integer(default=0, description='The ID of the article'),
        'article_comment_id': fields.Integer(default=0, description='The ID of the article comment'),
        'activity': fields.Integer(enum=[x.value for x in TimelineActivity], attribute='activity.value', default=False)
    })
    
    timeline_model_response = api.model(name + '_' + 'model_response', {
        'id': fields.Integer(readonly=True, description=''),
        'user': fields.Nested(model_timeline_user, description='The user information'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'question_comment_id': fields.Integer(default=0, description='The ID of the question comment'),
        'answer_id': fields.Integer(default=0, description='The ID of the answer'),
        'answer_comment_id': fields.Integer(default=0, description='The ID of the answer comment'),
        'article_id': fields.Integer(default=0, description='The ID of the article'),
        'article_comment_id': fields.Integer(default=0, description='The ID of the article comment'),
        'activity': fields.Integer(enum=[x.value for x in TimelineActivity], attribute='activity.value', default=False),
        'activity_date': fields.DateTime(description='The activity datetime'),
    })