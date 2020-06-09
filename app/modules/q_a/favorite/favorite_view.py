from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .favorite_dto import FavoriteDto
from .favorite_controller import FavoriteController
from ...auth.decorator import admin_token_required, token_required

api = FavoriteDto.api
favorite = FavoriteDto.model


@api.route('')
class FavoriteList(Resource):
    @admin_token_required
    # @api.marshal_list_with(favorite)
    def get(self):
        '''
        Get list of comments from database.

        :return: The list of comments.
        '''
        controller = FavoriteController()
        return controller.get()

    @token_required
    @api.expect(favorite)
    # @api.marshal_with(favorite)
    def post(self):
        '''
        Create new comment.

        :return: The new comment if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = FavoriteController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Favorite(Resource):
    @token_required
    # @api.marshal_with(favorite)
    def get(self, id):
        '''
        Get comment by its ID.

        :param comment_id: The ID of the comment.

        :return: The comment with the specific ID.
        '''
        controller = FavoriteController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(favorite)
    # @api.marshal_with(favorite)
    def put(self, id):
        '''
        Update existing comment by its ID.

        :param comment_id: The ID of the comment which need to be updated.

        :return: The updated comment if success and null vice versa.
        '''
        data = api.payload
        controller = FavoriteController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete comment by its ID.

        :param comment_id: The ID of the comment.

        :return:
        '''
        controller = FavoriteController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search favorites by user_id (who favorites)')
parser.add_argument('favorited_user_id', type=str, required=False,
                    help='Search favorites by favorited_user_id (who has been favorited.)')
parser.add_argument('question_id', type=str, required=False, help='Search all favorites by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all favorites by answer_id.')
parser.add_argument('comment_id', type=str, required=False, help='Search all favorites by comment_id.')
parser.add_argument('from_date', type=str, required=False, help='Search all favorites by start favorited date.')
parser.add_argument('to_date', type=str, required=False, help='Search all favorites by finish favorited date.')


@api.route('/search')
@api.expect(parser)
class FavoriteSearch(Resource):
    @token_required
    def get(self):
        """
        Search all favorites that satisfy conditions.
        ---------------------

        :user_id: Search favorites by user_id

        :question_id: Search all favorites by question ID.

        :answer_id: Search favorites by answer ID.

        :return: List of comments.
        """
        args = parser.parse_args()
        controller = FavoriteController()
        return controller.search(args=args)
