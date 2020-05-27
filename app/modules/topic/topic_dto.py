from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class TopicDto(Dto):
    name = 'topic'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(requried=False),
        'name': fields.String(),
        'count': fields.Integer(),
        'user_id': fields.Integer(),
        'question_count': fields.Integer(),
        'user_count': fields.Integer(),
        'answer_count': fields.Integer(),
        'parent_id':fields.Integer(),
        'is_fixed':fields.Boolean(default=False),
        'created_date':fields.DateTime()
    })
