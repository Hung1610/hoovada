from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .answer_dto import AnswerDto
from .answer_controller import AnswerController
from ...auth.decorator import admin_token_required, token_required

api = AnswerDto.api
answer = AnswerDto.model


@api.route('')
class AnswerList(Resource):
    @admin_token_required
    # @api.marshal_list_with(answer)
    def get(self):
        '''
        Get the list of answers from database.

        :return: List of answers.
        '''
        controller = AnswerController()
        return controller.get()

    @token_required
    @api.expect(answer)
    # @api.marshal_with(answer)
    def post(self):
        '''
        Create new answer.

        :return: The answer if success and null vice versa.
        '''
        data = api.payload
        controller = AnswerController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Answer(Resource):
    @token_required
    # @api.marshal_with(answer)
    def get(self, id):
        '''
        Get the answer by its ID.

        :param id: The ID of the answer.

        :return:
        '''
        controller = AnswerController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(answer)
    # @api.marshal_with(answer)
    def put(self, id):
        '''
        Update the existing answer by its ID.

        :param id: The ID of the answer.

        :return:
        '''
        data = api.payload
        controller = AnswerController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete existing answer by its ID.
        :param id:
        :return:
        '''
        controller = AnswerController()
        return controller.delete(object_id=id)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
parser.add_argument('question_id', type=str, required=False, help='Search all answers by question_id.')
parser.add_argument('created_date', type=str, required=False, help='Search answers by created-date.')
parser.add_argument('updated_date', type=str, required=False, help='Search answers by updated-date.')
parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')


@api.route('/search')
@api.expect(parser)
class AnswerSearch(Resource):
    @token_required
    def get(self):
        """
        Search all topics that satisfy conditions.
        ---------------------

        :user_id: Search answers by user_id (who created question)

        :question_id: Search all topics by fixed topic ID.

        :created_date: Search by created date.

        :updated_date: Search by updated date.

        :from_date: Search answers created after this date.

        :to_date: Search answers created before this date.

        :return: List of buyers
        """
        args = parser.parse_args()
        controller = AnswerController()
        return controller.search(args=args)