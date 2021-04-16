#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
# third-party modules
from flask_restx import inputs, reqparse
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
        'display_name': fields.String(required=False, min_length=1, default=''),

        'first_name': fields.String(required=False, default=''),
        'middle_name': fields.String(required=False, default=''),
        'last_name': fields.String(required=False, default=''),

        'birthday': fields.DateTime(required=False),
        'is_birthday_hidden': fields.Boolean(required=False),
        'gender': fields.String(required=False, default=''),
        'age': fields.String(required=False, default=''),
        'email': fields.String(required=False),
        'password': fields.String(required=False),

        'profile_pic_url': fields.String(required=False, default=''),
        'cover_pic_url': fields.String(required=False, default=''),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
        'admin': fields.Boolean(required=False),
        'active': fields.Boolean(required=False, default=False),

        'about_me': fields.String(required=False, default=''),

        'show_email_publicly_setting': fields.Boolean(required=False, default=False),
        'hoovada_digests_setting': fields.Boolean(required=False, default=0),
        'hoovada_digests_frequency_setting': fields.String(required=False, default=''),

        'new_answer_notify_settings': fields.Boolean(required=False, default=False),
        'new_answer_email_settings': fields.Boolean(required=False, default=False),
        'my_question_notify_settings': fields.Boolean(required=False, default=False),
        'my_question_email_settings': fields.Boolean(required=False, default=False),
        'new_question_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_question_comment_email_settings': fields.Boolean(required=False, default=False),
        'new_answer_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_answer_comment_email_settings': fields.Boolean(required=False, default=False),
        'new_article_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_article_comment_email_settings': fields.Boolean(required=False, default=False),
        'question_invite_notify_settings': fields.Boolean(required=False, default=False),
        'question_invite_email_settings': fields.Boolean(required=False, default=False),
        'follow_notify_settings': fields.Boolean(required=False, default=False),
        'follow_email_settings': fields.Boolean(required=False, default=False),
        'followed_new_publication_notify_settings': fields.Boolean(required=False, default=False),
        'followed_new_publication_email_settings': fields.Boolean(required=False, default=False),

        'friend_request_notify_settings': fields.Boolean(required=False, default=True),
        'friend_request_email_settings': fields.Boolean(required=False, default=True),

        'admin_interaction_notify_settings': fields.Boolean(required=False, default=True),
        'admin_interaction_email_settings': fields.Boolean(required=False, default=True),

        'is_private': fields.Boolean(default=False, description='The user is private or not'),
        'is_deactivated': fields.Boolean(default=False, description='The user is deactivated or not'),
        'show_nsfw': fields.Boolean(default=True, description='The user wants nsfw topics shown or not'),

        'show_fullname_instead_of_display_name': fields.Boolean(required=False, default=True),

        'is_first_log_in': fields.Boolean(required=False, default=True),
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
        'is_birthday_hidden': fields.Boolean(required=False),
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
        'document_pic_url': fields.String(required=False, default=''),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
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

        'new_answer_notify_settings': fields.Boolean(required=False, default=False),
        'new_answer_email_settings': fields.Boolean(required=False, default=False),
        'my_question_notify_settings': fields.Boolean(required=False, default=False),
        'my_question_email_settings': fields.Boolean(required=False, default=False),
        'new_question_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_question_comment_email_settings': fields.Boolean(required=False, default=False),
        'new_answer_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_answer_comment_email_settings': fields.Boolean(required=False, default=False),
        'new_article_comment_notify_settings': fields.Boolean(required=False, default=False),
        'new_article_comment_email_settings': fields.Boolean(required=False, default=False),
        'question_invite_notify_settings': fields.Boolean(required=False, default=False),
        'question_invite_email_settings': fields.Boolean(required=False, default=False),
        'follow_notify_settings': fields.Boolean(required=False, default=False),
        'follow_email_settings': fields.Boolean(required=False, default=False),
        'followed_new_publication_notify_settings': fields.Boolean(required=False, default=False),
        'followed_new_publication_email_settings': fields.Boolean(required=False, default=False),

        'friend_request_notify_settings': fields.Boolean(required=False, default=True),
        'friend_request_email_settings': fields.Boolean(required=False, default=True),

        'admin_interaction_notify_settings': fields.Boolean(required=False, default=True),
        'admin_interaction_email_settings': fields.Boolean(required=False, default=True),

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
        
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),

        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
        
        'show_fullname_instead_of_display_name': fields.Boolean(required=False, default=True),
        'is_first_log_in': fields.Boolean(required=False, default=True),
    })
    
    model_social_response = api.model('user_social_response', {
        'id': fields.Integer(readonly=True),
        'user_id': fields.Integer(required=False),
        'provider': fields.String(required=False),
        'uid': fields.String(required=False),
        'extra_data': fields.String(required=False),
    })

    model_user_mention_request = reqparse.RequestParser().copy()
    model_user_mention_request.add_argument('user_mentioned_id', type=list, required=True, help='user mention to')

    model_get_social_account_parser = api.parser()
    model_get_social_account_parser.add_argument('provider', type=str, required=False, help='Search social account by provider name')

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('display_name', type=str, required=False, help='Search user by display name')
    model_get_parser.add_argument('email', type=str, required=False, help='Search user by email')
    model_get_parser.add_argument('email_or_name', type=str, required=False, help='Search user by email')
    model_get_parser.add_argument('endorsed_topic_id', type=int, required=False, help='Get user endorsed status by id')
    model_get_parser.add_argument('is_endorsed', type=inputs.boolean, required=False, help='Get all endorsed users in database.')
    model_get_parser.add_argument('is_mutual_friend', type=inputs.boolean, required=False, help='Get mutual friends in database.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'question_count', 'post_count', 'answer_count', 'reputation'", type=str,
                            choices=('question_count', 'post_count', 'answer_count', 'reputation'), action='append',)
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields:  'question_count', 'post_count', 'answer_count', 'reputation'", type=str,
                            choices=( 'question_count', 'post_count', 'answer_count', 'reputation'), action='append',)



    model_topic = api.model('topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_user = api.model('user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        'profile_views': fields.Integer(default=False, description='User view count'),
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
    })


    answer_question = api.model('answer_question', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'slug': fields.String(description='The slug of the question'),
        'user_id': fields.Integer(description='The user ID', attribute='display_user_id'),
        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'user': fields.Nested(model_user, description='The user information', attribute='display_user'),        
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
    })

    model_article = api.model('article', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the article'),
        'slug': fields.String(description='The slug of the article'),   
        'html': fields.String(description='The content of the article'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of article views'),
        'last_activity': fields.DateTime(description='The last time this article was updated.'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_anonymous': fields.Boolean(default=False, description='The article is anonymous or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
        'scheduled_date': fields.DateTime(description='The scheduled date'),
        'user': fields.Nested(model_user, description='The user information'),
        'fixed_topic': fields.Nested(model_topic, description='The fixed topic'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
    })

    model_question = api.model('question', {
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
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'allow_video_answer': fields.Boolean(default=False, description='The question allows video answer or not'),
        'allow_audio_answer': fields.Boolean(default=False, description='The question allows audio answer or not'),
        'is_private': fields.Boolean(default=False, description='The question is private or not'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'invited_users': fields.List(fields.Nested(model_user), description='The list of invited users'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
        'user': fields.Nested(model_user, description='The user information', attribute='display_user'),
        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
    })

    model_answer = api.model('answer', {
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
        'up_vote': fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote': fields.Boolean(default=False, description='The value of downvote of current user'),
        'file_url': fields.String(description='The file url'),
        'file_type': fields.String(description='The file type', attribute='file_type.name'),
        'is_anonymous': fields.Boolean(default=False, description='The question is anonymous or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
        'user': fields.Nested(model_user, description='The user information', attribute='display_user'),        
        'question': fields.Nested(answer_question, description='The question information'),
        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
        'allow_improvement': fields.Boolean(default=True, description='The answer allows improvement suggestion or not'),

    })

    model_post = api.model('post', {
        'id': fields.Integer(readonly=True, description=''),
        'user': fields.Nested(model_user, description='The user information'),
        'html': fields.String(description='The content of the post'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of post views'),
        'last_activity': fields.DateTime(description='The last time this post was updated.'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_deleted': fields.Boolean(default=False, description='The post is soft deleted or not'),
        'file_url': fields.String(description='The file url'),
        'allow_favorite': fields.Boolean(default=False, description='Allow liking or not'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
    })

    model_poll_user_select = api.model('model_poll_user_select', {
        'user': fields.Nested(model_user, description='The detail of owner user'),
    })

    model_poll_select = api.model('poll_select', {
        'content': fields.String(description='The content of selection of a poll'),
        'poll_user_selects': fields.List(fields.Nested(model_poll_user_select), description='The list of users selecting'),
        'created_by_user': fields.Nested(model_user, description='User that select this selection')
    })
    
    model_poll = api.model('poll', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        'title': fields.String(default=None, description='The title of the poll'),
        'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
        'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
        'poll_select_count': fields.Integer(description='Total count of selections'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'poll_selects': fields.Nested(model_poll_select, description='List all selections of a poll'),
        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
        'own_user': fields.Nested(model_user, description='The detail of owner user'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
    })

    model_article_list = api.model('article_list', {
        'article_list' : fields.List(fields.Nested(model_article), required=False, allow_none=True, allow_empty=True, description='List of articles'),   
        'blog_name' : fields.String(required=False,  allow_none=True, allow_empty=True, description='Name of list of blogs'),
        'total' : fields.Integer(required=False, allow_none=True, allow_empty=True, description='Number of blogs in this list')
    })

    model_user_feed_all_response = api.model('feed_all_response', {
        'feed_type': fields.String(required=False),
        'article' : fields.Nested(model_article_list, required=False, allow_none=True, allow_empty=True),
        'question' : fields.Nested(model_question, required=False, allow_none=True, allow_empty=True),
        'post' : fields.Nested(model_post, required=False, allow_none=True, allow_empty=True),
        'answer' : fields.Nested(model_answer, required=False, allow_none=True, allow_empty=True),
        'poll' : fields.Nested(model_poll, required=False, allow_none=True, allow_empty=True),
        'ranked_score': fields.Float(required=False),
    })

    model_article_feed_response = api.model('article_feed_response', {
        'article_list': fields.List(fields.Integer(required=False), required=False),
        'blog_name': fields.String(required=False),
        'total': fields.Integer(required=False),
    })

    model_user_feed_response = api.model('user_feed_response', {
        'feed_type': fields.String(required=False),
        'article': fields.Nested(model_article_feed_response, required=False),
        'question_id': fields.Integer(required=False),
        'answer_id': fields.Integer(required=False),
        'post_id': fields.Integer(required=False),
        'poll_id': fields.Integer(required=False),
        'ranked_score': fields.Float(required=False),
    })

    model_user_feed_request = Dto.paginated_request_parser.copy()