#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

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

    model_request = api.model('answer_request', {
        'anonymous': fields.Boolean(default=False, description='The answer was created by anonymous'),
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'user_id': fields.Integer(default=0, description='The user ID'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'user_hidden': fields.Boolean(default=False, description='The answer was created by user but in hidden mode')
    })

    model_response = api.model('answer_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the answer'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date answer was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date answer was updated'),
        'last_activity': fields.DateTime(default=datetime.utcnow, description='The last time answer was updated'),

        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),

        'anonymous': fields.Boolean(default=False, description='The answer was created by anonymous'),
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        # 'user_id': fields.Integer(default=0, description='The user ID'),
        'user':fields.Nested(answer_user, description='The information of the user'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        # 'image_ids': fields.String(),
        'user_hidden': fields.Boolean(default=False, description='The answer was created by user but in hidden mode'),
        'comment_count': fields.Integer(default=0, description='The amount of comments on this answer'),
        'share_count': fields.Integer(default=0, description='The amount of shares on this answer'),
        'up_vote': fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote': fields.Boolean(default=False, description='The value of downvote of current user')
    })
