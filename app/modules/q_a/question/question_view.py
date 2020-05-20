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
        controller = QuestionController()
        return controller.get()

    # @token_required
    @api.expect(question)
    @api.marshal_with(question)
    def post(self):
        data = api.payload
        controller = QuestionController()
        return controller.create(data=data)


@api.route('/<int:question_id>')
class Question(Resource):
    # @token_required
    @api.marshal_with(question)
    def get(self, question_id):
        controller = QuestionController()
        return controller.get_by_id(object_id=question_id)

    # @token_required
    @api.expect(question)
    @api.marshal_with(question)
    def put(self, question_id):
        data = api.payload
        controller = QuestionController()
        return controller.update(object_id=question_id, data=data)

    # @token_required
    def delete(self, question_id):
        controller = QuestionController()
        return controller.delete(object_id=question_id)
