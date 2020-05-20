from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .comment_dto import CommentDto
from .comment_controller import CommentController

api = CommentDto.api
comment = CommentDto.model


@api.route('')
class CommentList(Resource):
    # @token_required
    @api.marshal_list_with(comment)
    def get(self):
        controller = CommentController()
        return controller.get()

    # @token_required
    @api.expect(comment)
    @api.marshal_with(comment)
    def post(self):
        data = api.payload
        controller = CommentController()
        return controller.create(data=data)


@api.route('/<int:comment_id>')
class Comment(Resource):
    # @token_required
    @api.marshal_with(comment)
    def get(self, comment_id):
        controller = CommentController()
        return controller.get_by_id(object_id=comment_id)

    # @token_required
    @api.expect(comment)
    @api.marshal_with(comment)
    def put(self, comment_id):
        data = api.payload
        controller = CommentController()
        return controller.update(object_id=comment_id, data=data)

    # @token_required
    def delete(self, comment_id):
        controller = CommentController()
        return controller.delete(object_id=comment_id)
