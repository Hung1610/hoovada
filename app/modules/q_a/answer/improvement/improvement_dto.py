#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AnswerImprovementDto(Dto):
    name = 'answer_improvement'
    api = Namespace(name, description="Answer improvement operations")

    answer_improvement_user = api.model('answer_improvement_user',{
        'id': fields.Integer(readonly=True, description = 'The user ID'),
        'display_name': fields.String(required=True, description = 'The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('answer_improvement_request', {
        'content': fields.String(description='The content of the answer'),
    })


    model_response = api.model('answer_improvement_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the answer'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date answer was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date answer was updated'),
        'last_activity': fields.DateTime(default=datetime.utcnow, description='The last time answer was updated'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'user_id': fields.Integer(description='The user ID', attribute='display_user_id'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'comment_count': fields.Integer(default=0, description='The amount of comments on this answer'),
        'share_count': fields.Integer(default=0, description='The amount of shares on this answer'),
        'file_url': fields.String(description='The file url'),
        'file_type': fields.String(description='The file type', attribute='file_type.name'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'user': fields.Nested(answer_improvement_user, description='The user information', attribute='display_user'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),        
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'is_upvoted_by_me':fields.Boolean(default=False, description='is upvoted by current user.'),
        'is_downvoted_by_me':fields.Boolean(default=False, description='is downvoted by current user.'),
    })

    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
    get_parser.add_argument('answer_id', type=str, required=False, help='Search all answers by answer_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',)
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',)
