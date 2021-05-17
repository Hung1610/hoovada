#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Namespace, fields

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFeedDto(Dto):
	name = 'user_feed'
	api = Namespace(name, description="User feed operations")

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
	    'user': fields.Nested(model_user, description='The user information'),
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
	    'user': fields.Nested(model_user, description='The user information'),        
	    'question': fields.Nested(model_question, description='The question information'),
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
	    'is_anonymous': fields.Boolean(default=False, description='The post is created anonymously'),
	    'file_url': fields.String(description='The file url'),
	    'allow_favorite': fields.Boolean(default=False, description='Allow liking or not'),
	    'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
	})

	model_poll_user_select = api.model('model_poll_user_select', {
		'id': fields.Integer(readonly=True, description='The ID of the poll user select'),
	    'user': fields.Nested(model_user, description='The detail of owner user'),
	})

	model_poll_select = api.model('poll_select', {
		'id': fields.Integer(readonly=True, description='The ID of the poll select'),
	    'content': fields.String(description='The content of selection of a poll'),
	    'poll_user_selects': fields.List(fields.Nested(model_poll_user_select), description='The list of users selecting'),
	    'user': fields.Nested(model_user, description='User that select this selection')
	})

	model_poll = api.model('poll', {
	    'id': fields.Integer(required=False, readonly=True, description='The ID of the poll'),
	    'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
	    'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
	    'user': fields.Nested(model_user, description='The detail of owner user'),
	    'title': fields.String(default=None, description='The title of the poll'),
		'slug': fields.String(default=None, description='The slug of the poll'),
	    'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
	    'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
	    'poll_select_count': fields.Integer(description='Total count of selections'),
	    'poll_selects': fields.Nested(model_poll_select, description='List all selections of a poll'),
	    'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
	    'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),

	    'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
	    'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
	    'share_count': fields.Integer(default=0, description='The amount of sharing'),
	    'comment_count': fields.Integer(default=0, description='The amount of comments'),
	    
	    'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
	    'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
	    'allow_selecting': fields.Boolean(default=True, description='Allow select or not'),

	    'is_anonymous': fields.Boolean(default=False, description='The poll is created anonymously'),
	})

	model_article_list = api.model('article_list', {
	    'article_list' : fields.List(fields.Nested(model_article), required=False, allow_none=True, allow_empty=True, description='List of articles'),   
	    'blog_name' : fields.String(required=False,  allow_none=True, allow_empty=True, description='Name of list of blogs'),
	    'total' : fields.Integer(required=False, allow_none=True, allow_empty=True, description='Number of blogs in this list')
	})

	model_feed_all_data_details_response = api.model('feed_all_data_details_response', {
	    'feed_type': fields.String(required=False),
	    'article' : fields.Nested(model_article_list, required=False, allow_none=True, allow_empty=True),
	    'question' : fields.Nested(model_question, required=False, allow_none=True, allow_empty=True),
	    'post' : fields.Nested(model_post, required=False, allow_none=True, allow_empty=True),
	    'answer' : fields.Nested(model_answer, required=False, allow_none=True, allow_empty=True),
	    'poll' : fields.Nested(model_poll, required=False, allow_none=True, allow_empty=True),
	    'ranked_score': fields.Float(required=False),
	})

	model_feed_all_data_response = api.model('feed_all_data_response', {
		'data' : fields.Nested(model_feed_all_data_details_response, description='Feed all data', required=False)
	})

	model_article_feed_response = api.model('article_feed_response', {
		'article_list': fields.List(fields.Integer(required=False), required=False),
		'blog_name': fields.String(required=False),
		'total': fields.Integer(required=False),
	})

	model_feed_details_response = api.model('feed_details_response', {
		'feed_type': fields.String(required=False),
		'article': fields.Nested(model_article_feed_response, required=False),
		'question_id': fields.Integer(required=False),
		'answer_id': fields.Integer(required=False),
		'post_id': fields.Integer(required=False),
		'poll_id': fields.Integer(required=False),
		'ranked_score': fields.Float(required=False),
	})

	model_feed_response = api.model('get_feed_all_response', {
		'data' : fields.Nested(model_feed_details_response, description='Feed', required=False)
	})


	model_user_feed_request = Dto.paginated_request_parser.copy()