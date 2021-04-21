#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# built-in modules
from datetime import datetime

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class PollBookmarkDto(Dto):
    name = 'poll_bookmark'
    api = Namespace(name, description="Poll bookmark operations")

    model_topic_poll_bookmark = api.model('topic_poll_bookmark', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_user = api.model('user', {
        'id': fields.Integer(readonly=True, description='The ID of the user'),
        'profile_pic_url': fields.String(description='The profile url of the user'),
        'display_name': fields.String(description='The display name url of the user'),
    })

    model_topic = api.model('topic_for_poll', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic'),
        'is_fixed': fields.Boolean(description='Is a fixed topic'),
    })

    model_poll_user_select = api.model('model_poll_user_select', {
        'user': fields.Nested(model_user, description='The detail of owner user'),
    })

    model_poll_select = api.model('poll_select', {
        'content': fields.String(description='The content of selection of a poll'),
        'poll_user_selects': fields.List(fields.Nested(model_poll_user_select), description='The list of users selecting'),
        'user': fields.Nested(model_user, description='User that select this selection')
    })

    model_poll = api.model('poll_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        "user": fields.Nested(model_user, description='The detail of owner user'),
        'title': fields.String(default=None, description='The title of the poll'),
        'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
        'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
        'poll_selects': fields.Nested(model_poll_select, description='List all selections of a poll'),
        'select_count': fields.Integer(default=0, description='Total count of selections'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
    })

    model_request = api.model('bookmark_poll_request', {
    })

    model_response = api.model('bookmark_poll_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who bookmarked'),
        'poll_id': fields.Integer(required=False, description='The user ID who has been bookmarked'),
        'poll':fields.Nested(model_poll, description='The information of the poll'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search bookmarks by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all bookmarks by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all bookmarks by finish voting date.')
    model_get_parser.add_argument('bookmarkd_user_id', type=str, required=False, help='Search bookmarks by user owner of the poll')
