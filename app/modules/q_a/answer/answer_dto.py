from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AnswerDto(Dto):
    name = 'answer'
    api = Namespace(name)
    model_request = api.model('answer_request', {
        'anonymous': fields.Boolean(default=False),
        'accepted': fields.Boolean(default=False),
        'answer': fields.String(),
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        'user_id': fields.Integer(),
        'question_id': fields.Integer(),
        'user_hidden':fields.Boolean(default=False)
    })

    model_response = api.model('answer_response', {
        'id': fields.Integer(required=False, readonly=True),
        'created_date': fields.DateTime(),
        'updated_date': fields.DateTime(),
        'last_activity': fields.DateTime(),

        'upvote_count': fields.Integer(),
        'downvote_count': fields.Integer(),

        'anonymous': fields.Boolean(default=False),
        'accepted': fields.Boolean(default=False),
        'answer': fields.String(),
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        'user_id': fields.Integer(),
        'question_id': fields.Integer(),
        # 'image_ids': fields.String(),
        'user_hidden':fields.Boolean(default=False)
    })
