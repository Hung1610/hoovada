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


class SearchDto(Dto):
    name = 'search'
    api = Namespace(name, description="Search operations")

    model_search_article_res = api.model('search_article_res', {
        'id': fields.Integer(readonly=True, description=''),
        'slug': fields.String(description='The slug of the article'),
        'title': fields.String(description='The title of the article'),
    })

    search_response = api.model('response', {
        'message': fields.String(required=True)
    })

    model_search_poll_response = api.model('search_poll_response', {
        'id': fields.Integer(readonly=True, description='Id of poll'),
        'title': fields.String(description='The title of the poll'),
    })

    model_search_user_response = api.model('search_user_response', {
        'id': fields.Integer(readonly=True, description='Id of user'),
        'display_name': fields.String(description='The display name of the user'),
        'email': fields.String(description='The email of the user'),
        'profile_pic_url': fields.String(description='The profile picture of the user'),
        'endorsed_count': fields.Integer(required=False),
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_search_question_response = api.model('search_question_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'question': fields.String(description='The content of the question'),
        'slug': fields.String(description='The slug of the question'),
        'answers_count': fields.Integer(readonly=True, description='Number of answers')
    })

    model_search_topic_response = api.model('search_topic_response', {
        'id': fields.Integer(readonly=True, description='Id of topic'),
        'name': fields.String(description='The name of the topic'),
        'slug': fields.String(description='The slug of the topic'),
    })

    model_search_user_friend_response = api.model('search_user_friend_response', {
        'id': fields.Integer(readonly=True, description='Id of user friend'),
        'friend_id': fields.Integer(readonly=True, description='Id of friend'),
        'friend_display_name': fields.String(readonly=True, description='Display name of friend'),
        'friend_email': fields.String(readonly=True, description='Email of friend'),
        'friend_profile_pic_url': fields.String(readonly=True, description='Profile picture url of friend'),
        'friended_id': fields.Integer(readonly=True, description='Id of friended'),
        'friended_display_name': fields.String(readonly=True, description='Display name of friended'),
        'friended_email': fields.String(readonly=True, description='Email of friended'),
        'friended_profile_pic_url': fields.String(readonly=True, description='Profile picture url of friended'),
        "is_approved": fields.Integer(readonly=True, description='Status of friend request'),
    })


    search_model_request_parser = reqparse.RequestParser()
    search_model_request_parser.add_argument('value', type=str, required=True, help='Value to search')
    search_model_request_parser.add_argument('from', type=str, required=False, help='From index')
    search_model_request_parser.add_argument('size', type=str, required=False, help='Number of records returned')

    search_user_request_parser = reqparse.RequestParser()
    search_user_request_parser.add_argument('value', type=str, required=True, help='Value to search')
    search_user_request_parser.add_argument('from', type=str, required=False, help='From index')
    search_user_request_parser.add_argument('size', type=str, required=False, help='Number of records returned')

    search_topic_request_parser = reqparse.RequestParser()
    search_topic_request_parser.add_argument('value', type=str, required=True, help='Value to search')
    search_topic_request_parser.add_argument('is_fixed', type=int, required=False, help='Set 1 to get only fixed_topic, 0 to get only non fixed_topic, do not set to get all')
    search_topic_request_parser.add_argument('from', type=str, required=False, help='From index')
    search_topic_request_parser.add_argument('size', type=str, required=False, help='Number of records returned')