from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class UserTopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name)
    model = api.model(name, {
        'user_topic_id': fields.Integer(required=False),
        'user_id': fields.Integer(),
        'topic_id': fields.Integer()
    })
