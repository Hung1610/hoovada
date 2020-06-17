from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class VoteDto(Dto):
    name = 'vote'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False, readonly=True, description=''),
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'up_vote': fields.Boolean(description=''),
        'down_vote': fields.Boolean(description=''),
        'voting_date': fields.DateTime(description=''),
        'modified_date': fields.DateTime(description='')
    })
