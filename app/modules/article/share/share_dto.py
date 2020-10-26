from flask_restx import fields, Namespace

from common.dto import Dto


class ShareDto(Dto):
    name = 'article_share'
    api = Namespace(name, description="Article sharing operations")

    model_request = api.model('article_share_request', {
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description='')
    })

    model_article = api.model('share_article',{
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the article'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
    })

    model_response = api.model('article_share_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'article_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description=''),
        'article': fields.Nested(model_article, description='The article information'),
    })
