from datetime import datetime

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
        'user_id': fields.Integer(default=0),
        'question_id': fields.Integer(default=0),
        'user_hidden': fields.Boolean(default=False)
    })

    model_response = api.model('answer_response', {
        'id': fields.Integer(required=False, readonly=True),
        'created_date': fields.DateTime(default=datetime.utcnow),
        'updated_date': fields.DateTime(default=datetime.utcnow),
        'last_activity': fields.DateTime(default=datetime.utcnow),

        'upvote_count': fields.Integer(default=0),
        'downvote_count': fields.Integer(default=0),

        'anonymous': fields.Boolean(default=False),
        'accepted': fields.Boolean(default=False),
        'answer': fields.String(),
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        'user_id': fields.Integer(default=0),
        'question_id': fields.Integer(default=0),
        # 'image_ids': fields.String(),
        'user_hidden': fields.Boolean(default=False),
        'comment_count': fields.Integer(default=0),
        'share_count': fields.Integer(default=0)
    })
