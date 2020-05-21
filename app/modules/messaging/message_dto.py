from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class MessageDto(Dto):
    name = 'message'
    api = Namespace(name)
    model = api.model(name, {
        'message_id': fields.Integer(required=False),
        'message': fields.DateTime(),
        'sent_time': fields.DateTime(),
        'read_time': fields.DateTime(),
        'sender_id': fields.Integer(),
        'recipient_id': fields.Integer()
    })
