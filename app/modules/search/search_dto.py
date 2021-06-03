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
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'friend_id': fields.Integer(required=False, description='The user ID who has sent friend request'),
        'friend':fields.Nested(model_search_user_response, description='The information of the user who sends friend request'),
        'friended_id': fields.Integer(required=False, description='The user ID who has been friendd'),
        'friended':fields.Nested(model_search_user_response, description='The information of the friended user'),
        'is_approved': fields.Boolean(default=False, description='This friend request is approved or not'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_post_response = api.model('search_post_response', {
        'id': fields.Integer(readonly=True, description=''),
        'user': fields.Nested(model_search_user_response, description='The user information'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of post views'),
        'last_activity': fields.DateTime(description='The last time this post was updated.'),
        
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_anonymous': fields.Boolean(default=False, description='The post is created anonymously'),
        'file_url': fields.String(description='The file url'),
        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_favorite': fields.Boolean(default=True, description='Allow favorite or not'),
        'highlighted_html': fields.String(description='The content including the keyword of the post'),
    })

    model_event_search_response = api.model('event_search_response', {
        'user': fields.Nested(model_search_user_response, description='The user information'),
        'question': fields.Nested(model_search_question_response, description='The question information'),
        'topic': fields.Nested(model_search_topic_response, description='The toppic information'),
        'article': fields.Nested(model_search_article_res, description='The article information'),
        'post': fields.Nested(model_post_response, description='The post information'),
        'polls': fields.Nested(model_search_poll_response, description='The poll information'),

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