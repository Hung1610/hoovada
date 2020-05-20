from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .answer_dto import AnswerDto
from .answer_controller import AnswerController

api = AnswerDto.api
answer = AnswerDto.model


@api.route('')
class answerList(Resource):
    # @token_required
    @api.marshal_list_with(answer)
    def get(self):
        controller = AnswerController()
        return controller.get()

    # @token_required
    @api.expect(answer)
    @api.marshal_with(answer)
    def post(self):
        data = api.payload
        controller = AnswerController()
        return controller.create(data=data)


@api.route('/<int:answer_id>')
class answer(Resource):
    # @token_required
    @api.marshal_with(answer)
    def get(self, answer_id):
        controller = AnswerController()
        return controller.get_by_id(object_id=answer_id)

    # @token_required
    @api.expect(answer)
    @api.marshal_with(answer)
    def put(self, answer_id):
        data = api.payload
        controller = AnswerController()
        return controller.update(object_id=answer_id, data=data)

    # @token_required
    def delete(self, answer_id):
        controller = AnswerController()
        return controller.delete(object_id=answer_id)
