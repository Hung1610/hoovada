from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class VoteDto(Dto):
    name = 'vote'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False, readonly=True),
        'user_id': fields.Integer(),
        'question_id': fields.Integer(),
        'answer_id': fields.Integer(),
        'comment_id': fields.Integer(),
        'up_vote': fields.Boolean(),
        'down_vote': fields.Boolean(),
        'voting_date': fields.DateTime(),
        'modified_date': fields.DateTime()
    })
