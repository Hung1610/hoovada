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
    name = 'article_comment'
    api = Namespace(name, description="Article comment operations")

    comment_user = api.model('article_comment_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('article_comment_request', {
        'comment': fields.String(required=True, description='The content of the comment'),
        'user_id': fields.Integer(required=True, description='The user ID')
    })

    model_response = api.model('article_comment_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the comment'),
        'comment': fields.String(required=True, description='The content of the comment'),
        'article_id': fields.Integer(required=True, description='The ID of the answer'),
        'user': fields.Nested(comment_user, description='The information of the user'),
        # 'user_id': fields.Integer(required=True, description='The user ID'),
        'updated_date': fields.DateTime(description='The date comment was updated'),
        'created_date': fields.DateTime(required=True, description='The date comment was created')
    })
