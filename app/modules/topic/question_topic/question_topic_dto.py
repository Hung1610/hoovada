from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionTopicDto(Dto):
    name = 'question_topic'
    api = Namespace(name)
    model_request = api.model('question_topic_request', {
        'question_id': fields.Integer(required=True, description='The ID of the question'),
        'topic_id': fields.Integer(required=True, description='The ID of the topic')
    })
    model_response = api.model('question_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of question topic record'),
        'question_id': fields.Integer(required=True, description='The ID of the question'),
        'topic_id': fields.Integer(required=True, description='The ID of the topic'),
        'created_date':fields.DateTime(description='The date question_topic record was created')
    })
