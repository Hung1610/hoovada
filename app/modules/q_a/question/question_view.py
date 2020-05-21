from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .question_dto import QuestionDto
from .question_controller import QuestionController

api = QuestionDto.api
question = QuestionDto.model


@api.route('')
class QuestionList(Resource):
    # @token_required
    @api.marshal_list_with(question)
    def get(self):
        '''
        Get list of questions from database.

        :return: List of questions.
        '''
        controller = QuestionController()
        return controller.get()

    # @token_required
    @api.expect(question)
    @api.marshal_with(question)
    def post(self):
        '''
        Create new question and save to database.

        :return: The question if success and None vice versa.
        '''
        data = api.payload
        controller = QuestionController()
        return controller.create(data=data)


@api.route('/<int:question_id>')
class Question(Resource):
    # @token_required
    @api.marshal_with(question)
    def get(self, question_id):
        '''
        Get specific question by its ID.

        :param question_id: The ID of the question to get from.

        :return: The question if success and None vice versa.
        '''
        controller = QuestionController()
        return controller.get_by_id(object_id=question_id)

    # @token_required
    @api.expect(question)
    @api.marshal_with(question)
    def put(self, question_id):
        '''
        Update existing question by its ID.

        :param question_id: The ID of the question.

        :return:
        '''
        data = api.payload
        controller = QuestionController()
        return controller.update(object_id=question_id, data=data)

    # @token_required
    def delete(self, question_id):
        '''
        Delete the question by its ID.

        :param question_id: The ID of the question.

        :return:
        '''
        controller = QuestionController()
        return controller.delete(object_id=question_id)
