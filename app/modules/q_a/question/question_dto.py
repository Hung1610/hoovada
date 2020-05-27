from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name)
    model = api.model(name, {
        'id':fields.Integer(required=False),
        'title':fields.String(),
        'user_id':fields.Integer(),
        'fixed_topic_id':fields.Integer(),
        'question':fields.String(),
        'markdown':fields.String(),
        'html':fields.String(),
        'created_date':fields.DateTime(),
        'updated_date':fields.DateTime(),
        'views': fields.Integer(),
        'last_activity':fields.DateTime(),
        'answers_allowed':fields.Integer(),
        'accepted_answer_id':fields.Integer(),
        'anonymous':fields.Boolean(default=False),
        'image_ids':fields.String()
    })
