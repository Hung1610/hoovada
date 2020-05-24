from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .comment_dto import CommentDto
from .comment_controller import CommentController
from ...auth.decorator import admin_token_required, token_required

api = CommentDto.api
comment = CommentDto.model


@api.route('')
class CommentList(Resource):
    @admin_token_required
    @api.marshal_list_with(comment)
    def get(self):
        '''
        Get list of comments from database.

        :return: The list of comments.
        '''
        controller = CommentController()
        return controller.get()

    @token_required
    @api.expect(comment)
    @api.marshal_with(comment)
    def post(self):
        '''
        Create new comment.

        :return: The new comment if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = CommentController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Comment(Resource):
    @token_required
    @api.marshal_with(comment)
    def get(self, id):
        '''
        Get comment by its ID.

        :param id: The ID of the comment.

        :return: The comment with the specific ID.
        '''
        controller = CommentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(comment)
    @api.marshal_with(comment)
    def put(self, id):
        '''
        Update existing comment by its ID.

        :param id: The ID of the comment which need to be updated.

        :return: The updated comment if success and null vice versa.
        '''
        data = api.payload
        controller = CommentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete comment by its ID.

        :param id: The ID of the comment.

        :return:
        '''
        controller = CommentController()
        return controller.delete(object_id=id)
