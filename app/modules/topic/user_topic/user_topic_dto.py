from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class UserTopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name)
    model_request = api.model('user_topic_request', {
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The topic ID')
    })
    model_response = api.model('user_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the user_topic record'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The topic ID'),
        'created_date':fields.DateTime(description='The date user_topic record was created.')
    })
