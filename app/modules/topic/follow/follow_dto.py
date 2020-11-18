#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicFollowDto(Dto):
    name = 'topic_follow'
    api = Namespace(name, description="Topic follow operations")

    model_follow_parent_topic = api.model('topic_topic_bookmark', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'article_count': fields.Integer(description='The amount of article belong to this topic'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'endorsers_count': fields.Integer(description='The amount of endorsers belong to this topic'),
        'bookmarkers_count': fields.Integer(description='The amount of bookmarkers belong to this topic'),
        'followers_count': fields.Integer(description='The amount of followers belong to this topic'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })

    model_follow_topic = api.model('follow_topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'parent': fields.Nested(model_follow_parent_topic, description='The parent (fixed) topic'),
        'article_count': fields.Integer(description='The amount of article belong to this topic'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'endorsers_count': fields.Integer(description='The amount of endorsers belong to this topic'),
        'bookmarkers_count': fields.Integer(description='The amount of bookmarkers belong to this topic'),
        'followers_count': fields.Integer(description='The amount of followers belong to this topic'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })

    model_request = api.model('follow_topic_request', {
    })

    model_response = api.model('follow_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who followd'),
        'topic_id': fields.Integer(required=False, description='The user ID who has been followd'),
        'topic':fields.Nested(model_follow_topic, description='The information of the topic'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search follows by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all follows by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all follows by finish voting date.')
    model_get_parser.add_argument('followed_user_id', type=str, required=False, help='Search follows by user owner of the topic')
