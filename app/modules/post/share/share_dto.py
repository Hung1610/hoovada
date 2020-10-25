from flask_restx import fields, Namespace

from common.dto import Dto


class ShareDto(Dto):
    name = 'post_share'
    api = Namespace(name, description="Post sharing operations")

    model_request = api.model('post_share_request', {
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description='')
    })

    model_post = api.model('share_post',{
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the post'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'html': fields.String(description='The content of the post'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
    })

    model_response = api.model('post_share_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'post_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'post': fields.Nested(model_post, description='The post information'),
    })
