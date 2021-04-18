from flask_restx import Namespace, fields

from common.dto import Dto

# built-in modules
from datetime import datetime


class ShareDto(Dto):
    name = 'poll_share'
    api = Namespace(name, description="Post sharing operations")

    model_request = api.model('poll_share_request', {
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description='')
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
        'user': fields.Nested(model_user, description='The info of creator'),
        'title': fields.String(default=None, description='The title of the poll'),
        'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
        'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
        'poll_selects': fields.Nested(model_poll_select, description='List all selections of a poll'),
        'select_count': fields.Integer(default=0, description='Total count of selections'),
        'upvote_count': fields.Integer(default=0, description='The number of upvote'),
        'downvote_count': fields.Integer(default=0, description='The number of downvote'),
        'share_count': fields.Integer(default=0, description='The number of sharing'),
        'comment_count': fields.Integer(default=0, description='The number of comments'),
    })

    model_response = api.model('poll_share_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'poll_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'poll': fields.Nested(model_poll, description='The poll information'),
    })
