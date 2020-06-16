from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class FavoriteDto(Dto):
    name = 'favorite'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False, readonly=True),
        'user_id': fields.Integer(required=True),
        'favorited_user_id': fields.Integer(required=False),
        'question_id': fields.Integer(required=False),
        'answer_id': fields.Integer(required=False),
        'comment_id': fields.Integer(required=False),
        'favorite_date': fields.DateTime(required=False)
    })
