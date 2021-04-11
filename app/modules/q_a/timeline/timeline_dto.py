#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.enum import TimelineActivityEnum
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class TimelineDto(Dto):
    name = 'timeline'
    api = Namespace(name, description="Question-Timeline operations")

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search timeline by user id')
    model_get_parser.add_argument('question_id', type=int, required=False, help='Search all timelines related to question id.')
    model_get_parser.add_argument('answer_id', type=int, required=False, help='Search all timelines related to answer id.')
    model_get_parser.add_argument('poll_id', type=int, required=False, help='Search all timelines related to poll id.')
    model_get_parser.add_argument('comment_id', type=int, required=False, help='Search all timelines related to comment id.')
    model_get_parser.add_argument('article_id', type=int, required=False, help='Search all timelines related to article id.')
    model_get_parser.add_argument('article_comment_id', type=int, required=False, help='Search all timelines related to article comment id.')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search timelines created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search timelines created before this data.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'activity_date'", type=str,
                            choices=('activity_date'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'activity_date'", type=str,
                            choices=('activity_date'), action='append',
                        )
    
    model_timeline_user = api.model(name + '_' + 'user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
        'profile_pic_url': fields.String(required=False),
    })

    timeline_model_request = api.model(name + '_' + 'model_request', {
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'question_comment_id': fields.Integer(default=0, description='The ID of the question comment'),
        'answer_id': fields.Integer(default=0, description='The ID of the answer'),
        'poll_id': fields.Integer(default=0, description='The ID of the poll'),
        'answer_comment_id': fields.Integer(default=0, description='The ID of the answer comment'),
        'article_id': fields.Integer(default=0, description='The ID of the article'),
        'article_comment_id': fields.Integer(default=0, description='The ID of the article comment'),
        'activity': fields.Integer(enum=[x.value for x in TimelineActivityEnum], attribute='activity.value', default=False)
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
        'poll_id': fields.Integer(default=0, description='The ID of the poll'),
        'poll_comment_id': fields.Integer(default=0, description='The ID of the poll comment'),
        'activity': fields.Integer(enum=[x.value for x in TimelineActivityEnum], attribute='activity.value', default=False),
        'activity_date': fields.DateTime(description='The activity datetime'),
    })