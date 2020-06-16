from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class TopicDto(Dto):
    name = 'topic'
    api = Namespace(name)

    model_sub_topic = api.model('sub_topic', {
        'id': fields.Integer(readonly=True),
        'name': fields.String(),
        'user_id': fields.Integer(),
        'question_count': fields.Integer(),
        'user_count': fields.Integer(),
        'created_date': fields.DateTime(),
        'description': fields.String()
    })

    # define the model for request
    model_topic_request = api.model('topic_request', {
        'name': fields.String(required=True),
        'parent_id': fields.Integer(required=True),
        'user_id': fields.Integer(required=True),
        'description': fields.String()
    })

    # define the model for response
    model_topic_response = api.model('topic_response', {
        'id': fields.Integer(requried=False, readonly=True),
        'name': fields.String(),
        'count': fields.Integer(),
        'user_id': fields.Integer(),
        'question_count': fields.Integer(),
        'user_count': fields.Integer(),
        'answer_count': fields.Integer(),
        'parent_id': fields.Integer(),
        'is_fixed': fields.Boolean(default=False),
        'created_date': fields.DateTime(),
        'description': fields.String(),
        'sub_topics': fields.List(fields.Nested(model_sub_topic))
    })
