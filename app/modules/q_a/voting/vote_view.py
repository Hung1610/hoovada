from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .vote_dto import VoteDto
from .vote_controller import VoteController
from ...auth.decorator import admin_token_required, token_required

api = VoteDto.api
vote = VoteDto.model


@api.route('')
class VoteList(Resource):
    @admin_token_required
    # @api.marshal_list_with(vote)
    def get(self):
        '''
        Get list of votes from database.

        :return: The list of votes.
        '''
        controller = VoteController()
        return controller.get()

    @token_required
    @api.expect(vote)
    # @api.marshal_with(vote)
    def post(self):
        '''
        Create new vote.

        :return: The new vote if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = VoteController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Vote(Resource):
    @token_required
    # @api.marshal_with(vote)
    def get(self, id):
        '''
        Get vote by its ID.

        :param id: The ID of the vote.

        :return: The vote with the specific ID.
        '''
        controller = VoteController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(vote)
    # @api.marshal_with(vote)
    def put(self, id):
        '''
        Update existing vote by its ID.

        :param id: The ID of the vote which need to be updated.

        :return: The updated vote if success and null vice versa.
        '''
        data = api.payload
        controller = VoteController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete vote by its ID.

        :param id: The ID of the vote.

        :return:
        '''
        controller = VoteController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search votes by user_id')
parser.add_argument('question_id', type=str, required=False, help='Search all votes by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all votes by answer_id.')
parser.add_argument('comment_id', type=str, required=False, help='Search all votes by comment_id.')
parser.add_argument('from_date', type=str, required=False, help='Search all votes by start voting date.')
parser.add_argument('to_date', type=str, required=False, help='Search all votes by finish voting date.')


@api.route('/search')
@api.expect(parser)
class VoteSearch(Resource):
    @token_required
    def get(self):
        """
        Search all votes that satisfy conditions.
        ---------------------

        :user_id: Search votes by user_id

        :question_id: Search all votes by question ID.

        :answer_id: Search votes by answer ID.

        :return: List of comments.
        """
        args = parser.parse_args()
        controller = VoteController()
        return controller.search(args=args)
