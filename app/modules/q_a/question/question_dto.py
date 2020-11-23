#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name, description="Question operations")

    model_topic = api.model('topic_for_question', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_question_user = api.model('question_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        'profile_views': fields.Integer(default=False, description='User view count'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_answer_request = api.model('answer_question_request', {
        'accepted': fields.Boolean(default=False, description='The answer was accepted or not'),
        'answer': fields.String(description='The content of the answer'),
        'allow_comments': fields.Boolean(default=True, description='The answer allows commenting or not'),
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    model_question_request = api.model('question_request', {
        'title': fields.String(description='The title of the question'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'topics': fields.List(fields.Integer, description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='The answer allows commenting or not'),
        'allow_video_answer': fields.Boolean(default=False, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=False, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=False, description='The question is private or not'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
        # the list of IDs of topics that question belongs to.
    })

    model_question_response = api.model('question_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'slug': fields.String(description='The slug of the question'),
        'user_id': fields.Integer(description='The user ID', attribute='display_user_id'),
        'user': fields.Nested(model_question_user, description='The user information', attribute='display_user'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        # the list of IDs of topics that question belongs to.
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comment'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'allow_comments': fields.Boolean(default=True, description='The answer allows commenting or not'),
        'allow_video_answer': fields.Boolean(default=False, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=False, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=False, description='The question is private or not'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'invited_users': fields.List(fields.Nested(model_question_user), description='The list of invited users'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    model_question_proposal_response = api.model('question_proposal_response', {
        'id': fields.Integer(readonly=True, description=''),
        'question_id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        # 'user_id': fields.Integer(description='The user ID'),
        'user': fields.Nested(model_question_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'slug': fields.String(description='The slug of the question'),
        'allow_video_answer': fields.Boolean(default=False, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=False, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=False, description='The question is private or not'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'invited_users': fields.List(fields.Nested(model_question_user), description='The list of invited users'),
        'is_approved': fields.Boolean(default=False, description='The question proposal is approved or not'),
        'proposal_created_date': fields.DateTime(description='The proposal created date'),
        'proposal_updated_date': fields.DateTime(description='The proposal updated date'),
    })

    top_user_reputation_args_parser = reqparse.RequestParser()
    top_user_reputation_args_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    top_user_reputation_args_parser.add_argument('topic', type=int, action='append', required=True, help='Relevant topics IDs')

    top_user_reputation_response = api.model('top_user_reputation_response', {
        'user': fields.Nested(model_question_user, description='The user information'),
        'total_score': fields.Integer(default=0, description='The total reputation score of user for relevant topics'),
    })

    question_invite_request = api.model('question_invite_request', {
        'emails_or_usernames': fields.List(fields.String, description='The list of emails/usernames to invite by'),
    })

    get_similar_questions_parser = reqparse.RequestParser()
    get_similar_questions_parser.add_argument('title', type=str, required=False, help='Title by which to get similar questions')
    get_similar_questions_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    get_similar_questions_parser.add_argument('exclude_question_id', type=str, required=False, help='Exclude question with this id')

    get_relevant_topics_parser = reqparse.RequestParser()
    get_relevant_topics_parser.add_argument('title', type=str, required=False, help='Title by which to get relevant topics')
    get_relevant_topics_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')


    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('title', type=str, required=False, help='Search question by its title')
    get_parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
    get_parser.add_argument('fixed_topic_id', type=str, required=False, help='Search all questions related to fixed-topic.')
    get_parser.add_argument('topic_id', type=str, required=False, action='append', help='Search all questions related to topic.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search questions created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search questions created before this data.')
    get_parser.add_argument('is_deleted', type=inputs.boolean, required=False, help='Search questions that are deleted.')
    get_parser.add_argument('is_shared', type=inputs.boolean, required=False, help='Search questions that are shared.')
    get_parser.add_argument('is_created_by_friend', type=inputs.boolean, required=False, help='Search questions that are created by friend/followee.')
    get_parser.add_argument('hot', type=inputs.boolean, required=False, help='Search questions that are hot.')
    get_parser.add_argument('for_me', type=inputs.boolean, required=False, help='Search questions that relevant for current user.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count', 'answer_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count', 'answer_count'), action='append',
                        )
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count', 'answer_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count', 'answer_count'), action='append',
                        )
                        