#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto
from app.modules.organization.organization_dto import OrganizationDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleDto(Dto):
    name = 'organization_article'
    api = Namespace(name, description="Article operations")

    model_topic = api.model('topic_for_article', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'slug': fields.String(description='The slug of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_article_user = api.model('article_user', {
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

    model_article_request = api.model('article_request', {
        'title': fields.String(description='The title of the article'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics'),
        'scheduled_date': fields.DateTime(description='The scheduled date'),
        'is_draft': fields.Boolean(default=False, description='The article is a draft or not'),
        'is_anonymous': fields.Boolean(default=False, description='The article is anonymous or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
        'organization_id': fields.String(description='The ID of organization who owns this article. Must be specified when sending the article to a organization'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
    })

    model_organization_article_response = api.model('organization_article_response', {
        'id': fields.Integer(readonly=True, description='The ID of the organization'),
        'display_name': fields.String(description='The display name of the organization'),
        'description': fields.String(description='The description of the organization'),
        'email': fields.String(description='The email of the organization'),
        'website_url': fields.String(description='The website url of the organization'),
        'status': fields.String(description='The current status of the organization'),
        'phone_number': fields.String(description='The phone number of the organization'),
        'logo_url': fields.String(description='The logo url of the organization'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'user_id': fields.Integer(description='The ID of user owner of the organization'),
        'user': fields.Nested(model_article_user, description='The user information'),
        'user_count': fields.Integer(description='Number of users joined the organization'),
        'article_count': fields.Integer(description='Number of articled published by the organization'),
        'is_joined_by_me': fields.Boolean(description='Is joined in the organization by me'),
    })

    model_article_response = api.model('article_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the article'),
        'slug': fields.String(description='The slug of the article'),   
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of article views'),
        'last_activity': fields.DateTime(description='The last time this article was updated.'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'is_anonymous': fields.Boolean(default=False, description='The article is anonymous or not'),
        'scheduled_date': fields.DateTime(description='The scheduled date'),
        'user': fields.Nested(model_article_user, description='The user information'),
        'fixed_topic': fields.Nested(model_topic, description='The fixed topic'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_comments': fields.Boolean(default=True, description='Allow commenting or not'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting or not'),
        'is_draft': fields.Boolean(default=False, description='The article is a draft or not'),
        'entity_type': fields.String(default='user', description='The own type of organization. Must be one of values user or organization'),
        'organization_id': fields.String(description='The ID of organization who owns this article. Must be specified when entity_type is organization'),
        'organization': fields.Nested(model_organization_article_response, description='The detail of organization'),

        'is_upvoted_by_me':fields.Boolean(default=False, description='is upvoted by current user.'),
        'is_downvoted_by_me':fields.Boolean(default=False, description='is downvoted by current user.'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='is bookmarked by current user.'),
    })

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('title', type=str, required=False, help='Search article by its title')
    model_get_parser.add_argument('fixed_topic_id', type=int, required=False, help='Search all articles related to fixed-topic.')
    model_get_parser.add_argument('topic_id', type=int, required=False, action='split', help='Search all articles from the list of topic ids')
    model_get_parser.add_argument('article_ids', type=int, required=False, action='split', help='Search all articles from the list of article ids')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search articles created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search articles created before this data.')
    model_get_parser.add_argument('draft', type=inputs.boolean, required=False, help='Search articles that are drafts.')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search all articles created by user.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count' ", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'), action='append',)
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count' ", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count'), action='append',)

    get_similar_articles_parser = reqparse.RequestParser()
    get_similar_articles_parser.add_argument('title', type=str, required=False, help='Title by which to get similar questions')
    get_similar_articles_parser.add_argument('fixed_topic_id', type=int, required=False, help='fixed_topic_id by which to get similar questions')
    get_similar_articles_parser.add_argument('topic_id', type=int, required=False, action='append', help='topic_id by which to get similar questions')
    get_similar_articles_parser.add_argument('limit', type=int, default=30, required=False, help='Limit amount to return')
    get_similar_articles_parser.add_argument('exclude_article_id', type=str, required=False, help='Exclude article with this id')