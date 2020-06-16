from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class UserTopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False, readonly=True),
        'user_id': fields.Integer(),
        'topic_id': fields.Integer()
    })
