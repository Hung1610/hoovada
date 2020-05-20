from app.modules.common.view import Resource
from .question_topic_dto import QuestionTopicDto
from .question_topic import QuestionTopic
from .question_topic_controller import QuestionTopicController

api = QuestionTopicDto.api
question_topic = QuestionTopicDto.model


@api.route('')
class UserTopicList(Resource):
    @api.marshal_list_with(question_topic)
    def get(self):
        pass

    @api.expect(question_topic)
    def post(self):
        pass


@api.route('/<int:question_topic_id>')
class UserTopic(Resource):
    @api.marshal_with(question_topic)
    def get(self, question_topic_id):
        pass

    @api.expect(question_topic)
    def post(self, question_topic_id):
        pass

    def delete(self, question_topic_id):
        pass
