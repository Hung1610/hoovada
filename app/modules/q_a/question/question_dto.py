#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name, description="Question operations")

    model_topic = api.model('topic_for_question', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_question_user = api.model('question_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        # 'title': fields.String(required=False),

        # 'first_name': fields.String(required=False),
        # 'middle_name': fields.String(required=False),
        # 'last_name': fields.String(required=False),
        # 'gender': fields.String(required=False),
        # 'age': fields.String(required=False),
        # 'email': fields.String(required=False),
        # 'password': fields.String(required=False),

        # 'last_seen': fields.DateTime(required=False),
        # 'joined_date': fields.DateTime(required=False),
        # 'confirmed': fields.Boolean(required=False),
        # 'email_confirmed_at': fields.DateTime(required=False),

        'profile_pic_url': fields.String(required=False)
        # 'profile_pic_data_url': fields.String(required=False),
        # 'admin': fields.Boolean(required=False),
        # 'active': fields.Boolean(required=False),

        # 'reputation': fields.Integer(required=False),
        # 'profile_views': fields.Integer(required=False, readonly=True),
        # 'city': fields.String(required=False),
        # 'country': fields.String(required=False),
        # 'website_url': fields.String(required=False),
        #
        # 'about_me': fields.String(required=False),
        # 'about_me_markdown': fields.String(required=False),
        # 'about_me_html': fields.String(required=False),
        #
        # 'people_reached': fields.Integer(required=False),
        # 'job_role': fields.String(required=False),
        # 'company': fields.String(required=False),

        # 'show_email_publicly_setting': fields.Boolean(required=False),
        # 'hoovada_digests_setting': fields.Boolean(required=False),
        # 'hoovada_digests_frequency_setting': fields.String(required=False),
        #
        # 'questions_you_asked_or_followed_setting': fields.Boolean(required=False),
        # 'questions_you_asked_or_followed_frequency_setting': fields.String(required=False),
        # 'people_you_follow_setting': fields.Boolean(required=False),
        # 'people_you_follow_frequency_setting': fields.String(required=False),
        #
        # 'email_stories_topics_setting': fields.Boolean(required=False),
        # 'email_stories_topics_frequency_setting': fields.String(required=False),
        # 'last_message_read_time': fields.DateTime(required=False),
        #
        # # count region
        # 'question_count': fields.Integer(required=False),
        # 'question_favorite_count': fields.Integer(required=False),
        # 'question_favorited_count': fields.Integer(required=False),
        # 'question_share_count': fields.Integer(required=False),
        # 'question_shared_count': fields.Integer(required=False),

        # 'answer_count': fields.Integer(required=False),
        # 'answer_share_count': fields.Integer(required=False),
        # 'answer_shared_count': fields.Integer(required=False),
        # 'answer_favorite_count': fields.Integer(required=False),
        # 'answer_favorited_count': fields.Integer(required=False),
        # 'answer_upvote_count': fields.Integer(required=False),
        # 'answer_upvoted_count': fields.Integer(required=False),
        # 'answer_downvote_count': fields.Integer(required=False),
        # 'answer_downvoted_count': fields.Integer(required=False),
        #
        # 'topic_follow_count': fields.Integer(required=False),
        # 'topic_followed_count': fields.Integer(required=False),
        # 'topic_created_count': fields.Integer(required=False),
        #
        # 'user_follow_count': fields.Integer(required=False),
        # 'user_followed_count': fields.Integer(required=False),
        #
        # 'comment_count': fields.Integer(required=False),
        # 'comment_upvote_count': fields.Integer(required=False),
        # 'comment_upvoted_count': fields.Integer(required=False),
        # 'comment_downvote_count': fields.Integer(required=False),
        # 'comment_downvoted_count': fields.Integer(required=False),
        # 'comment_report_count': fields.Integer(required=False),
        # 'comment_reported_count': fields.Integer(required=False)

    })

    model_question_request = api.model('question_request', {
        'title': fields.String(description='The title of the question'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'anonymous': fields.Boolean(default=False, description='The question was created by anonymous'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The question wss created by user but the user want to be hidden'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics'),
        'allow_video_answer': fields.Boolean(default=True, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=True, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=True, description='The question is private or not'),
        # the list of IDs of topics that question belongs to.
    })

    model_question_response = api.model('question_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        # 'user_id': fields.Integer(description='The user ID'),
        'user': fields.Nested(model_question_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        # 'markdown': fields.String(description=''),
        # 'html': fields.String(description=''),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'anonymous': fields.Boolean(default=False, description='The question was created by anonymous'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The question wss created by user but the user want to be hidden'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        # the list of IDs of topics that question belongs to.
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'slug': fields.String(description='The slug of the question'),
        'allow_video_answer': fields.Boolean(default=True, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=True, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=True, description='The question is private or not'),
        'invited_users': fields.List(fields.Nested(model_question_user), description='The list of invited users'),
        # 'image_ids':fields.String()
    })

    model_question_proposal_response = api.model('question_proposal_response', {
        'id': fields.Integer(readonly=True, description=''),
        'question_id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        # 'user_id': fields.Integer(description='The user ID'),
        'user': fields.Nested(model_question_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        # 'markdown': fields.String(description=''),
        # 'html': fields.String(description=''),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'anonymous': fields.Boolean(default=False, description='The question was created by anonymous'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The question wss created by user but the user want to be hidden'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        # the list of IDs of topics that question belongs to.
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'slug': fields.String(description='The slug of the question'),
        'allow_video_answer': fields.Boolean(default=True, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=True, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=True, description='The question is private or not'),
        'invited_users': fields.List(fields.Nested(model_question_user), description='The list of invited users'),
        'is_approved': fields.Boolean(default=True, description='The question proposal is approved or not'),
        'proposal_created_date': fields.DateTime(description='The proposal created date'),
        'proposal_updated_date': fields.DateTime(description='The proposal updated date'),
        # 'image_ids':fields.String()
    })

    top_user_reputation_args_parser = reqparse.RequestParser()
    top_user_reputation_args_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    top_user_reputation_args_parser.add_argument('topic', type=int, action='append', required=True, help='Relevant topics IDs')

    top_user_reputation_response = api.model('top_user_reputation_response', {
        'user': fields.Nested(model_question_user, description='The user information'),
        'total_score': fields.Integer(default=0, description='The total reputation score of user for relevant topics'),
    })

    question_invite_request = api.model('question_invite_request', {
        'emails_or_usernames': fields.List(fields.Integer, description='The list of emails/usernames to invite by'),
    })

    get_similar_questions_parser = reqparse.RequestParser()
    get_similar_questions_parser.add_argument('title', type=str, required=False, help='Title by which to get similar questions')
    get_similar_questions_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')

    get_relevant_topics_parser = reqparse.RequestParser()
    get_relevant_topics_parser.add_argument('title', type=str, required=False, help='Title by which to get relevant topics')
    get_relevant_topics_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
