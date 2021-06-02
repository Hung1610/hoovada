#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AnswerDto(Dto):
    name = 'answer'
    api = Namespace(name, description="Answer operations")

    answer_user = api.model('answer_user',{
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        'profile_views': fields.Integer(default=False),
        'endorsed_count': fields.Integer(required=False),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),    
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_topic = api.model('topic_for_question', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    answer_question = api.model('answer_question', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'slug': fields.String(description='The slug of the question'),
        'user_id': fields.Integer(description='The user ID', attribute='display_user_id'),
        'question': fields.String(description='The content of the question'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'comment_count': fields.Integer(default=0, description='The amount of comment'),
        'allow_video_answer': fields.Boolean(default=False, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=False, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=False, description='The question is private or not'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),

        'is_upvoted_by_me':fields.Boolean(default=False, description='is upvoted by current user.'),
        'is_downvoted_by_me':fields.Boolean(default=False, description='is downvoted by current user.'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='is bookmarked by current user.'),
    })


    model_request = api.model('answer_request', {
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'user_education_id': fields.Integer(required=False, description='The ID of the user education'),
        'user_topic_id': fields.Integer(required=False, description='The ID of the user topic'),
        'user_language_id': fields.Integer(required=False, description='The ID of the user language'),
        'user_location_id': fields.Integer(required=False, description='The ID of the user location'),
        'user_employment_id': fields.Integer(required=False, description='The ID of the user employment'),
        'is_anonymous': fields.Boolean(default=False, description='The answer is anonymous or not'),
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
    })

    model_user_education = api.model('model_user_education', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the education'),
        'school': fields.String(required=True, description='The content of the education'),
        'primary_major': fields.String(required=True, description='The content of the education'),
        'secondary_major': fields.String(required=False, description='The content of the education'),
        'is_current': fields.Boolean(default=False, description='The education is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(answer_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date education was updated'),
        'created_date': fields.DateTime(required=True, description='The date education was created'),
        'is_visible': fields.Boolean(default=False, description='Display the education or not')
    })


    model_user_location = api.model('model_user_location', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the location'),
        'location_detail': fields.String(required=True, description='The content of the location'),
        'is_current': fields.Boolean(default=False, description='The location is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(answer_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date location was updated'),
        'created_date': fields.DateTime(required=True, description='The date location was created'),
        'is_visible': fields.Boolean(default=False, description='Display the location or not')
    })


    model_language = api.model('language_for_user', {
        'id': fields.Integer(readonly=True, description='The ID of the language'),
        'name': fields.String(description='The name of the language'),
        'description': fields.String(description='Description about language')
    })


    model_user_language = api.model('model_user_language', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the language'),
        'language_id': fields.Integer(description='The ID of the parent language'),
        'language': fields.Nested(model_language, description='The information of the user'),
        'level': fields.String(required=True, description='The level of proficiency of the user for the language'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(answer_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date language was updated'),
        'created_date': fields.DateTime(required=True, description='The date language was created'),
        'is_visible': fields.Boolean(default=False, description='Display the language or not')
    })


    model_user_employment = api.model('model_user_employment', {
        'id': fields.Integer(required=False, readonly=True, description='The ID'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'position': fields.String(required=True, description='The position'),
        'company': fields.String(required=True, description='The company'),
        'start_year': fields.Integer(description='The start year'),
        'end_year': fields.Integer(description='The end year'),
        'is_current': fields.Integer(description='The currently work'),
        'created_date':fields.DateTime(description='The date user_employment record was created.'),
        'is_visible': fields.Boolean(default=False, description='Display the user employment or not')
    })

    model_user_topic = api.model('model_user_topic', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the topic'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic', attribute='topic.parent.id'),
        'fixed_topic': fields.Nested(model_topic, description='The information of the user', attribute='topic.parent'),
        'topic_id': fields.Integer(description='The ID of the parent topic'),
        'topic': fields.Nested(model_topic, description='The information of the user'),
        'description': fields.String(required=True, description='The content of the topic'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(answer_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date topic was updated'),
        'created_date': fields.DateTime(required=True, description='The date topic was created'),
        'is_visible': fields.Boolean(default=False, description='Display the topic or not')
    })

    model_response = api.model('answer_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the answer'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date answer was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date answer was updated'),
        'last_activity': fields.DateTime(default=datetime.utcnow, description='The last time answer was updated'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'user_id': fields.Integer(description='The user ID', attribute='display_user_id'),
        'question_id': fields.Integer(default=0, description='The ID of the question'),
        'comment_count': fields.Integer(default=0, description='The amount of comments on this answer'),
        'share_count': fields.Integer(default=0, description='The amount of shares on this answer'),
        'file_url': fields.String(description='The file url'),
        'file_type': fields.String(description='The file type', attribute='file_type.name'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'user': fields.Nested(answer_user, description='The user information', attribute='display_user'),
        'question': fields.Nested(answer_question, description='The question information'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),        
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'user_education': fields.Nested(model_user_education,default={},  skip_none=True,  description='The user info about education'),
        'user_location': fields.Nested(model_user_location,default={},  skip_none=True,  description='The user info about location'),
        'user_language': fields.Nested(model_user_language,default={},  skip_none=True,  description='The user info about language'),
        'user_employment': fields.Nested(model_user_employment,default={}, skip_none=True, description='The user info about employment'),
        'user_topic': fields.Nested(model_user_topic,skip_none=True,default={}, description='The user info about topic'),

        'is_upvoted_by_me':fields.Boolean(default=False, description='is upvoted by current user.'),
        'is_downvoted_by_me':fields.Boolean(default=False, description='is downvoted by current user.'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='is bookmarked by current user.'),
    })

    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
    upload_parser.add_argument('file_type', location='form', choices=(1, 2), help='1 - Audio, 2 - Video', type=str, required=True)


    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
    get_parser.add_argument('question_id', type=str, required=False, help='Search all answers by question_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'), action='append')
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'), action='append')

