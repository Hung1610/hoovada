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

class AnswerDto(Dto):
    name = 'answer'
    api = Namespace(name, description="Answer operations")

    answer_user = api.model('answer_user',{
        'id': fields.Integer(readonly=True, description = 'The user ID'),
        'display_name': fields.String(required=True, description = 'The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_comment_request = api.model('comment_answer_request', {
        'comment': fields.String(required=True, description='The content of the comment'),
        # 'question_id': fields.Integer(required=False),
    })

    model_request = api.model('answer_request', {
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'allow_comments': fields.Boolean(default=True, description='The answer allows commenting or not'),
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    model_response = api.model('answer_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the answer'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date answer was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date answer was updated'),
        'last_activity': fields.DateTime(default=datetime.utcnow, description='The last time answer was updated'),

        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        # 'user_id': fields.Integer(default=0, description='The user ID'),
        'user':fields.Nested(answer_user, description='The information of the user'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'comment_count': fields.Integer(default=0, description='The amount of comments on this answer'),
        'share_count': fields.Integer(default=0, description='The amount of shares on this answer'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorites on this answer'),
        'up_vote': fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote': fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'allow_comments': fields.Boolean(default=True, description='The answer allows commenting or not'),
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'file_url': fields.String(description='The file url'),
        'file_type': fields.String(description='The file type', attribute='file_type.name'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files',
                        type=FileStorage, required=True)
    upload_parser.add_argument('file_type', location='form', 
                        choices=(1, 2), help='1 - Audio, 2 - Video',
                        type=str, required=True)

    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
    get_parser.add_argument('question_id', type=str, required=False, help='Search all answers by question_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')
    get_parser.add_argument('is_deleted', type=bool, required=False, help='Search answers that are deleted.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count'), action='append',
                        )
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count'), action='append',
                        )
