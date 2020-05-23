from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .answer_dto import AnswerDto
from .answer_controller import AnswerController
from ...auth.decorator import admin_token_required, token_required

api = AnswerDto.api
answer = AnswerDto.model


@api.route('')
class AnswerList(Resource):
    @admin_token_required
    @api.marshal_list_with(answer)
    def get(self):
        '''
        Get the list of answers from database.

        :return: List of answers.
        '''
        controller = AnswerController()
        return controller.get()

    @token_required
    @api.expect(answer)
    @api.marshal_with(answer)
    def post(self):
        '''
        Create new answer.

        :return: The answer if success and null vice versa.
        '''
        data = api.payload
        controller = AnswerController()
        return controller.create(data=data)


@api.route('/<int:answer_id>')
class Answer(Resource):
    @token_required
    @api.marshal_with(answer)
    def get(self, answer_id):
        '''
        Get the answer by its ID.

        :param answer_id: The ID of the answer.

        :return:
        '''
        controller = AnswerController()
        return controller.get_by_id(object_id=answer_id)

    @token_required
    @api.expect(answer)
    @api.marshal_with(answer)
    def put(self, answer_id):
        '''
        Update the existing answer by its ID.

        :param answer_id: The ID of the answer.

        :return:
        '''
        data = api.payload
        controller = AnswerController()
        return controller.update(object_id=answer_id, data=data)

    @token_required
    def delete(self, answer_id):
        '''
        Delete existing answer by its ID.
        :param answer_id:
        :return:
        '''
        controller = AnswerController()
        return controller.delete(object_id=answer_id)
