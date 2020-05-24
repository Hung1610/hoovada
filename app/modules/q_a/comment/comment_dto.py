from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class CommentDto(Dto):
    name = 'comment'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False),
        'comment_body': fields.String(),
        'created_date': fields.DateTime(),
        'question_id': fields.Integer(),
        'answer_id': fields.Integer(),
        'user_id': fields.Integer()
    })
