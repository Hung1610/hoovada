from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .favorite_dto import FavoriteDto
from .favorite_controller import FavoriteController
from ...auth.decorator import admin_token_required, token_required

api = FavoriteDto.api
favorite = FavoriteDto.model


@api.route('')
class CommentList(Resource):
    @admin_token_required
    @api.marshal_list_with(favorite)
    def get(self):
        '''
        Get list of comments from database.

        :return: The list of comments.
        '''
        controller = FavoriteController()
        return controller.get()

    @token_required
    @api.expect(favorite)
    @api.marshal_with(favorite)
    def post(self):
        '''
        Create new comment.

        :return: The new comment if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = FavoriteController()
        return controller.create(data=data)


@api.route('/<int:favorite_id>')
class Comment(Resource):
    @token_required
    @api.marshal_with(favorite)
    def get(self, favorite_id):
        '''
        Get comment by its ID.

        :param comment_id: The ID of the comment.

        :return: The comment with the specific ID.
        '''
        controller = FavoriteController()
        return controller.get_by_id(object_id=favorite_id)

    @token_required
    @api.expect(favorite)
    @api.marshal_with(favorite)
    def put(self, favorite_id):
        '''
        Update existing comment by its ID.

        :param comment_id: The ID of the comment which need to be updated.

        :return: The updated comment if success and null vice versa.
        '''
        data = api.payload
        controller = FavoriteController()
        return controller.update(object_id=favorite_id, data=data)

    @token_required
    def delete(self, favorite_id):
        '''
        Delete comment by its ID.

        :param comment_id: The ID of the comment.

        :return:
        '''
        controller = FavoriteController()
        return controller.delete(object_id=favorite_id)
