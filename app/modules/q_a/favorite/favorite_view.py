from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .favorite_dto import FavoriteDto
from .favorite_controller import FavoriteController
from ...auth.decorator import admin_token_required, token_required

api = FavoriteDto.api
favorite_request = FavoriteDto.model_request
favorite_response = FavoriteDto.model_response


# @api.route('')
# class FavoriteList(Resource):
#     # @admin_token_required
#     # # @api.marshal_list_with(favorite)
#     # def get(self):
#     #     '''
#     #     Get list of favorites from database.
#     #
#     #     :return: The list of comments.
#     #     '''
#     #     controller = FavoriteController()
#     #     return controller.get()
#
#     @token_required
#     @api.expect(favorite_request)
#     @api.response(code=200, model=favorite_response, description='The model response for favorite.')
#     def post(self):
#         '''
#         Create new favorite.
#
#         :return: The new comment if it was created successfully and null vice versa.
#         '''
#         data = api.payload
#         controller = FavoriteController()
#         return controller.create(data=data)


# @api.route('/<int:id>')
class Favorite(Resource):
    @token_required
    @api.param(name='id', description='The favorite ID')
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def get(self, id):
        '''
        Get favorite by its ID.

        :param comment_id: The ID of the comment.

        :return: The comment with the specific ID.
        '''
        controller = FavoriteController()
        return controller.get_by_id(object_id=id)

    # @token_required
    # @api.expect(favorite_request)
    # @api.response(code=200, model=favorite_response, description='The model for favorite.')
    # def put(self, id):
    #     '''
    #     Update existing comment by its ID.
    #
    #     :param comment_id: The ID of the comment which need to be updated.
    #
    #     :return: The updated comment if success and null vice versa.
    #     '''
    #     data = api.payload
    #     controller = FavoriteController()
    #     return controller.update(object_id=id, data=data)

    # @token_required
    # def delete(self, id):
    #     '''
    #     Delete comment by its ID.
    #
    #     :param comment_id: The ID of the comment.
    #
    #     :return:
    #     '''
    #     controller = FavoriteController()
    #     return controller.delete(object_id=id)


@api.route('/user')
class FavoriteUser(Resource):
    @token_required
    @api.expect(favorite_request)
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def post(self):
        '''
        Create a favorite on user.

        :param data: The data in dictionary form.

        :return: The favorite if success and null vice versa.
        '''
        controller = FavoriteController()
        data = api.payload
        return controller.create_favorite_user(data=data)

    @token_required
    @api.param(name='id', description='The ID of the favorite to delete.')
    def delete(self, id):
        '''
        Delete favorite on user.

        :param id: The ID of the favorite to delete.

        :return: True if success and False vice versa.
        '''
        controller = FavoriteController()
        return controller.delete_favorite_user(object_id=id)


@api.route('/question')
class FavoriteQuestion(Resource):
    @token_required
    @api.expect(favorite_request)
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def post(self):

        controller = FavoriteController()
        data = api.payload
        return controller.create_favorite_question(data=data)

    @token_required
    @api.param(name='id', description='The ID of the favorite to delete.')
    def delete(self, id):
        controller = FavoriteController()
        return controller.delete_favorite_question(object_id=id)


@api.route('/answer')
class FavoriteAnswer(Resource):
    @token_required
    @api.expect(favorite_request)
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def post(self):
        controller = FavoriteController()
        data = api.payload
        return controller.create_favorite_answer(data=data)

    @token_required
    @api.param(name='id', description='The ID of the favorite to delete.')
    def delete(self, id):
        controller = FavoriteController()
        return controller.delete_favorite_answer(object_id=id)


@api.route('/comment')
class FavoriteComment(Resource):
    @token_required
    @api.expect(favorite_request)
    @api.response(code=200, model=favorite_response, description='The model for favorite.')
    def post(self):
        controller = FavoriteController()
        data = api.payload
        return controller.create_favorite_comment(data=data)

    @token_required
    @api.param(name='id', description='The ID of the favorite to delete.')
    def delete(self, id):
        controller = FavoriteController()
        return controller.delete_favorite_comment(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search favorites by user_id (who favorites)')
parser.add_argument('favorited_user_id', type=str, required=False,
                    help='Search favorites by favorited_user_id (who has been favorited.)')
parser.add_argument('question_id', type=str, required=False, help='Search all favorites by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all favorites by answer_id.')
parser.add_argument('comment_id', type=str, required=False, help='Search all favorites by comment_id.')
parser.add_argument('from_date', type=str, required=False, help='Search all favorites by start_favorited_date.')
parser.add_argument('to_date', type=str, required=False, help='Search all favorites by finish_favorited_date.')


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
