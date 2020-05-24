from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .question_topic_dto import QuestionTopicDto
from .question_topic_controller import QuestionTopicController
from ...auth.decorator import admin_token_required, token_required

api = QuestionTopicDto.api
question_topic = QuestionTopicDto.model


@api.route('')
class QuestionTopicList(Resource):
    @admin_token_required
    @api.marshal_list_with(question_topic)
    def get(self):
        '''
        Get list of question_topics from database.

        :return: The list of question_topics.
        '''
        controller = QuestionTopicController()
        return controller.get()

    @token_required
    @api.expect(question_topic)
    @api.marshal_with(question_topic)
    def post(self):
        '''
        Create new question_topic.

        :return: The new question_topic if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = QuestionTopicController()
        return controller.create(data=data)


@api.route('/<int:id>')
class QuestionTopic(Resource):
    @token_required
    @api.marshal_with(question_topic)
    def get(self, id):
        '''
        Get question_topic by its ID.

        :param id: The ID of the question_topic.

        :return: The question_topic with the specific ID.
        '''
        controller = QuestionTopicController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(question_topic)
    @api.marshal_with(question_topic)
    def put(self, id):
        '''
        Update existing question_topic by its ID.

        :param id: The ID of the question_topic which need to be updated.

        :return: The updated question_topic if success and null vice versa.
        '''
        data = api.payload
        controller = QuestionTopicController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete question_topic by its ID.

        :param id: The ID of the question_topic.

        :return:
        '''
        controller = QuestionTopicController()
        return controller.delete(object_id=id)
