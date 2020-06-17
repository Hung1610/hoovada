from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class CommentDto(Dto):
    name = 'comment'
    api = Namespace(name)
    model_requesst = api.model('comment_request', {
        'comment': fields.String(required=True),
        # 'question_id': fields.Integer(required=False),
        'answer_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=True)
    })

    model_response = api.model('comment_response', {
        'id': fields.Integer(required=False, readonly=True),
        'comment': fields.String(),
        'created_date': fields.DateTime(),
        # 'question_id': fields.Integer(),
        'answer_id': fields.Integer(),
        'user_id': fields.Integer(),
        'updated_date': fields.DateTime()
    })
