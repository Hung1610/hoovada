#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party module
from flask_restx import fields, Namespace

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerShareDto(Dto):
    name = 'answer_share'
    api = Namespace(name, description="Answer-Share operations")

    model_answer = api.model('share_answer',{
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
        'answer_id': fields.Integer(default=0, description='The ID of the answer'),
        # 'image_ids': fields.String(),
        'user_hidden': fields.Boolean(default=False, description='The answer was created by user but in hidden mode'),
        'comment_count': fields.Integer(default=0, description='The amount of comments on this answer'),
        'share_count': fields.Integer(default=0, description='The amount of shares on this answer')
    })


    model_request = api.model('share_answer_request', {
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'anonymous': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Integer(description='')
    })

    model_response = api.model('share_answer_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'anonymous': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'answer': fields.Nested(model_answer, description='The user information'),
    })
