from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionTopicDto(Dto):
    name = 'question_topic'
    api = Namespace(name)
    model = api.model(name, {
        'question_topic_id': fields.Integer(required=False),
        'question_id': fields.Integer(),
        'topic_id': fields.Integer()
    })
