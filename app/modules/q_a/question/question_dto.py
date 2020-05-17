from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name)
    model = api.model(name, {
        'question_id':fields.Integer(required=False),
        'title':fields.String(),
        'user_id':fields.Integer(),
        '_question':fields.String(),
        '_markdown':fields.String(),
        '_html':fields.String(),
        'created_date':fields.DateTime(),
        'updated_date':fields.DateTime(),
        'views': fields.Integer(),
        'last_activity':fields.DateTime(),
        'answers_allowed':fields.Integer(),
        'accepted_answer_id':fields.Integer(),
        'anonymous':fields.Boolean(),
        'image_ids':fields.String()
    })
