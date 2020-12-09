#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields

# own module
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserDto(Dto):
    name = 'user'
    api = Namespace(name, description='user related operations')
    model_request = api.model('user_request', {
        'display_name': fields.String(required=False, default=''),
        'title': fields.String(required=False, default=''),

        'first_name': fields.String(required=False, default=''),
        'middle_name': fields.String(required=False, default=''),
        'last_name': fields.String(required=False, default=''),

        'birthday': fields.DateTime(required=False),
        'gender': fields.String(required=False, default=''),
        'age': fields.String(required=False, default=''),
        'email': fields.String(required=True),
        'password': fields.String(required=True),

        'profile_pic_url': fields.String(required=False, default=''),
        'cover_pic_url': fields.String(required=False, default=''),
        'admin': fields.Boolean(required=False),
        'active': fields.Boolean(required=False, default=False),

        'reputation': fields.Integer(required=False, default=0),
        # 'profile_views': fields.Integer(required=False, readonly=True),

        'about_me': fields.String(required=False, default=''),
        'about_me_markdown': fields.String(required=False, default=''),
        'about_me_html': fields.String(required=False, default=''),

        'people_reached': fields.Integer(required=False, default=0),

        'show_email_publicly_setting': fields.Boolean(required=False, default=False),
        'hoovada_digests_setting': fields.Boolean(required=False, default=0),
        'hoovada_digests_frequency_setting': fields.String(required=False, default=''),

        'questions_you_asked_or_followed_setting': fields.Boolean(required=False, default=False),
        'questions_you_asked_or_followed_frequency_setting': fields.String(required=False, default=''),
        'people_you_follow_setting': fields.Boolean(required=False, default=False),
        'people_you_follow_frequency_setting': fields.String(required=False, default=''),

        'email_stories_topics_setting': fields.Boolean(required=False, default=False),
        'email_stories_topics_frequency_setting': fields.String(required=False, default=''),
        'is_private': fields.Boolean(default=False, description='The user is private or not'),
        'is_deactivated': fields.Boolean(default=False, description='The user is deactivated or not'),
        'show_nsfw': fields.Boolean(default=True, description='The user wants nsfw topics shown or not'),
        # 'last_message_read_time': fields.DateTime(required=False)
    })

    model_response = api.model('user_response', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'title': fields.String(required=False),
        'phone_number': fields.String(required=False),

        'first_name': fields.String(required=False),
        'middle_name': fields.String(required=False),
        'last_name': fields.String(required=False),

        'birthday': fields.DateTime(required=False),
        'gender': fields.String(required=False),
        'age': fields.String(required=False),
        'email': fields.String(required=False),
        # 'password': fields.String(required=False),

        'last_seen': fields.DateTime(required=False),
        'joined_date': fields.DateTime(required=False),
        'confirmed': fields.Boolean(required=False),
        'email_confirmed_at': fields.DateTime(required=False),

        'profile_pic_url': fields.String(required=False),
        'cover_pic_url': fields.String(required=False, default=''),
        'admin': fields.String(required=False),
        'permissions': fields.String(required=False),
        'active': fields.Boolean(required=False),

        'reputation': fields.Integer(required=False),
        'profile_views': fields.Integer(required=False, readonly=True),

        'about_me': fields.String(required=False),
        'about_me_markdown': fields.String(required=False),
        'about_me_html': fields.String(required=False),

        'people_reached': fields.Integer(required=False),

        'show_email_publicly_setting': fields.Boolean(required=False),
        'hoovada_digests_setting': fields.Boolean(required=False),
        'hoovada_digests_frequency_setting': fields.String(required=False),

        'questions_you_asked_or_followed_setting': fields.Boolean(required=False),
        'questions_you_asked_or_followed_frequency_setting': fields.String(required=False),
        'people_you_follow_setting': fields.Boolean(required=False),
        'people_you_follow_frequency_setting': fields.String(required=False),

        'email_stories_topics_setting': fields.Boolean(required=False),
        'email_stories_topics_frequency_setting': fields.String(required=False),
        'last_message_read_time': fields.DateTime(required=False),

        # count region
        'question_count': fields.Integer(required=False),
        'question_favorite_count': fields.Integer(required=False),
        'question_favorited_count': fields.Integer(required=False),
        'question_share_count': fields.Integer(required=False),
        'question_shared_count': fields.Integer(required=False),
        'question_report_count': fields.Integer(required=False),
        'question_reported_count': fields.Integer(required=False),

        'answer_count': fields.Integer(required=False),
        'answer_share_count': fields.Integer(required=False),
        'answer_shared_count': fields.Integer(required=False),
        'answer_favorite_count': fields.Integer(required=False),
        'answer_favorited_count': fields.Integer(required=False),
        'answer_upvote_count': fields.Integer(required=False),
        'answer_upvoted_count': fields.Integer(required=False),
        'answer_downvote_count': fields.Integer(required=False),
        'answer_downvoted_count': fields.Integer(required=False),
        'answer_report_count': fields.Integer(required=False),
        'answer_reported_count': fields.Integer(required=False),

        'topic_follow_count': fields.Integer(required=False),
        'topic_followed_count': fields.Integer(required=False),
        'topic_created_count': fields.Integer(required=False),

        'user_follow_count': fields.Integer(required=False),
        'user_followed_count': fields.Integer(required=False),

        'comment_count': fields.Integer(required=False),
        'comment_upvote_count': fields.Integer(required=False),
        'comment_upvoted_count': fields.Integer(required=False),
        'comment_downvote_count': fields.Integer(required=False),
        'comment_downvoted_count': fields.Integer(required=False),
        'comment_report_count': fields.Integer(required=False),
        'comment_reported_count': fields.Integer(required=False),

        'article_count': fields.Integer(required=False),

        'friend_count': fields.Integer(required=False),

        'endorsed_count': fields.Integer(required=False),

        'user_report_count': fields.Integer(required=False),
        'user_reported_count': fields.Integer(required=False),
        'is_private': fields.Boolean(default=False, description='The user is private or not'),
        'is_deactivated': fields.Boolean(default=False, description='The user is deactivated or not'),
        'show_nsfw': fields.Boolean(default=True, description='The user wants nsfw topics shown or not'),
        'is_online': fields.Boolean(default=False, description='The user is online or not'),

        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('display_name', type=str, required=False, help='Search user by display name')
    model_get_parser.add_argument('email', type=str, required=False, help='Search user by email')
    model_get_parser.add_argument('email_or_name', type=str, required=False, help='Search user by email')
    model_get_parser.add_argument('endorsed_topic_id', type=int, required=False, help='Get user endorsed status by id')
    model_get_parser.add_argument('is_endorsed', type=inputs.boolean, required=False, help='Get all endorsed users in database.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'question_count', 'post_count', 'answer_count'", type=str,
                            choices=('question_count', 'post_count', 'answer_count'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields:  'question_count', 'post_count', 'answer_count'", type=str,
                            choices=( 'question_count', 'post_count', 'answer_count'), action='append',
                        )
