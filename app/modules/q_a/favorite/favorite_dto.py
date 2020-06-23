from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class FavoriteDto(Dto):
    name = 'favorite'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False, readonly=True, description=''),
        'user_id': fields.Integer(required=True, description=''),
        'favorited_user_id': fields.Integer(required=False, description=''),
        'question_id': fields.Integer(required=False, description=''),
        'answer_id': fields.Integer(required=False, description=''),
        'comment_id': fields.Integer(required=False, description=''),
        'favorite_date': fields.DateTime(required=False, description='')
    })
