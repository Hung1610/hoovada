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
        """
        Get list of question-topic mappings from database.

        Note: This functions is used with administration right only

        :return: List of user-topic mappings.
        """
        controller = QuestionTopicController()
        return controller.get()

    @api.expect(question_topic)
    def post(self):
        """
        Create new question-topic mapping.

        :return: Question-topic mapping if success, False vice versa.
        """
        data = api.payload
        controller = QuestionTopicController()
        return controller.create(data=data)


@api.route('/<int:question_topic_id>')
class UserTopic(Resource):
    @api.marshal_with(question_topic)
    def get(self, question_topic_id):
        """
        Get question-topic mapping by its ID.

        :param question_topic_id: The unique ID of question-topic mapping.

        :return:
        """
        controller = QuestionTopicController()
        return controller.get_by_id(object_id=question_topic_id)

    @api.expect(question_topic)
    def put(self, question_topic_id):
        '''
        Update existing question-topic mapping.

        :param question_topic_id: The unique ID of question-topic mapping.

        :return:
        '''
        data = api.payload
        controller = QuestionTopicController()
        return controller.update(object_id=question_topic_id, data=data)

    def delete(self, question_topic_id):
        '''
        Delete question-topic mapping by its ID.

        :param question_topic_id: The ID of question-topic mapping.

        :return:
        '''
        controller = QuestionTopicController()
        return controller.delete(object_id=question_topic_id)
