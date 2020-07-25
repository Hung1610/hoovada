#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CommentDto(Dto):
    name = 'comment'
    api = Namespace(name)
    comment_user = api.model('comment_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_requesst = api.model('comment_request', {
        'comment': fields.String(required=True, description='The content of the comment'),
        # 'question_id': fields.Integer(required=False),
        'answer_id': fields.Integer(required=True, description='The ID of the answer'),
        'user_id': fields.Integer(required=True, description='The user ID')
    })

    model_response = api.model('comment_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the comment'),
        'comment': fields.String(required=True, description='The content of the comment'),
        'created_date': fields.DateTime(required=True, description='The date comment was created'),
        # 'question_id': fields.Integer(),
        'answer_id': fields.Integer(required=True, description='The ID of the answer'),
        'user': fields.Nested(comment_user, description='The information of the user'),
        # 'user_id': fields.Integer(required=True, description='The user ID'),
        'updated_date': fields.DateTime(description='The date comment was updated'),
        'upvote_count': fields.Integer(description='The amount of upvote'),
        'downvote_count': fields.Integer(description='The amount of downvote'),
        'report_count': fields.Integer(description='The amount of report')
    })
