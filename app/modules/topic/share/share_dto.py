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


class TopicShareDto(Dto):
    name = 'topic_share'
    api = Namespace(name, description="Topic-Share operations")

    model_topic = api.model('share_topic',{
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })


    model_request = api.model('share_topic_request', {
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Integer(description='')
    })

    model_response = api.model('share_topic_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'topic_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'topic': fields.Nested(model_topic, description='The user information'),
    })
