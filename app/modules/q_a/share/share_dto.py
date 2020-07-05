from flask_restx import fields, Namespace

from app.modules.common.dto import Dto


class ShareDto(Dto):
    name = 'share'
    api = Namespace(name)

    model_request = api.model('share_request', {
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'anonymous': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Integer(description='')
    })

    model_response = api.model('share_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'created_date': fields.DateTime(description=''),
        'facebook': fields.Boolean(description=''),
        'twitter': fields.Boolean(description=''),
        'linkedin': fields.Boolean(description=''),
        'zalo': fields.Boolean(description=''),
        'vkontakte': fields.Boolean(description=''),
        'anonymous': fields.Boolean(description=''),
        'mail': fields.Boolean(description=''),
        'link_copied': fields.Boolean(description='')
    })
