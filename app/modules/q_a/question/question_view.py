from datetime import datetime

from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .question_dto import QuestionDto
from .question_controller import QuestionController
from ...auth.decorator import admin_token_required, token_required

api = QuestionDto.api
question = QuestionDto.model


@api.route('')
class QuestionList(Resource):
    @admin_token_required
    # @api.marshal_list_with(question)
    def get(self):
        '''
        Get list of questions from database.

        :return: List of questions.
        '''
        controller = QuestionController()
        return controller.get()

    @token_required
    @api.expect(question)
    # @api.marshal_with(question)
    def post(self):
        '''
        Create new question and save to database.

        :return: The question if success and None vice versa.
        '''
        data = api.payload
        controller = QuestionController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Question(Resource):
    @token_required
    # @api.marshal_with(question)
    def get(self, id):
        '''
        Get specific question by its ID.

        :param id: The ID of the question to get from.

        :return: The question if success and None vice versa.
        '''
        controller = QuestionController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(question)
    # @api.marshal_with(question)
    def put(self, id):
        '''
        Update existing question by its ID.

        :param id: The ID of the question.

        :return:
        '''
        data = api.payload
        controller = QuestionController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete the question by its ID.

        :param id: The ID of the question.

        :return:
        '''
        controller = QuestionController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=False, help='Search question by its title')
parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
parser.add_argument('fixed_topic_id', type=str, required=False, help='Search all questions related to fixed-topic.')
parser.add_argument('created_date', type=str, required=False, help='Search questions by created-date.')
parser.add_argument('updated_date', type=str, required=False, help='Search questions by updated-date.')
parser.add_argument('from_date', type=str, required=False, help='Search questions created later that this date.')
parser.add_argument('to_date', type=str, required=False, help='Search questions created before this data.')
parser.add_argument('anonymous', type=str, required=False, help='Search questions created by Anonymous.')


@api.route('/search')
@api.expect(parser)
class QuesstionSearch(Resource):
    @token_required
    def get(self):
        """
        Search all questions that satisfy conditions.
        ---------------------
        :title: The name of the topics to search

        :user_id: Search questions by user_id (who created question)

        :fixed_topic_id: Search all questions by fixed topic ID.

        :created_date: Search by created date.

        :updated_date: Search by updated date.

        :from_date: Search questions created after this date.

        :to_date: Search questions created before this date.

        :anonymous: Search questions created by anonymous.

        :return: List of buyers
        """
        args = parser.parse_args()
        controller = QuestionController()
        return controller.search(args=args)
