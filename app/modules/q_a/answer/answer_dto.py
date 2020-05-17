from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AnswerDto(Dto):
    name = 'answer'
    api = Namespace(name)
    model = api.model(name, {
        'answer_id': fields.Integer(required=False),
        'created_date': fields.DateTime(),
        'update_date': fields.DateTime(),
        'last_activity': fields.DateTime(),

        'upvote_count': fields.Integer(),
        'downvote_count': fields.Integer(),

        'anonymous': fields.Integer(),
        'accepted': fields.Boolean(),
        '_answer_body': fields.String(),
        '_markdown': fields.String(),
        '_html': fields.String(),
        'user_id': fields.Integer(),
        'question_id': fields.Integer(),
        'image_ids': fields.String()
    })
