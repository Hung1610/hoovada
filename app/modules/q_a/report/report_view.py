from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .report_dto import ReportDto
from .report_controller import ReportController
from ...auth.decorator import admin_token_required, token_required

api = ReportDto.api
report_request = ReportDto.model_request
report_response = ReportDto.model_response


# @api.route('')
# class ReportingList(Resource):
#     @admin_token_required
#     @api.marshal_list_with(report_response)
#     def get(self):
#         '''
#         Get list of reportings from database.
#
#         :return: The list of reportings.
#         '''
#         controller = ReportController()
#         return controller.get()
#
#     @token_required
#     @api.expect(report_response)
#     @api.marshal_with(report_response)
#     def post(self):
#         '''
#         Create new report.
#
#         :return: The new report if it was created successfully and null vice versa.
#         '''
#         data = api.payload
#         controller = ReportController()
#         return controller.create(data=data)

@api.route('/user')
class ReportUser(Resource):
    @token_required
    @api.expect(report_request)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def post(self):
        controller = ReportController()
        data = api.payload
        return controller.create_report_user(data=data)


@api.route('/question')
class ReportQuestion(Resource):
    @token_required
    @api.expect(report_request)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def post(self):
        controller = ReportController()
        data = api.payload
        return controller.create_report_question(data=data)


@api.route('/answer')
class ReportAnswer(Resource):
    @token_required
    @api.expect(report_request)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def post(self):
        controller = ReportController()
        data = api.payload
        return controller.create_report_answer(data=data)


@api.route('/comment')
class ReportUser(Resource):
    @token_required
    @api.expect(report_request)
    @api.response(code=200, model=report_response, description='The model for report response.')
    def post(self):
        controller = ReportController()
        data = api.payload
        return controller.create_report_comment(data=data)


@api.route('/detail')
class Reporting(Resource):
    @token_required
    @api.param(name='id', description='The ID of report.')
    @api.response(code=200, model=report_response, description='The model for report response.')
    def get(self, id):
        '''
        Get report by its ID.

        :param id: The ID of the report.

        :return: The report with the specific ID.
        '''
        controller = ReportController()
        return controller.get_by_id(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search reports by user_id')
parser.add_argument('question_id', type=str, required=False, help='Search all reports by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all reports by answer_id.')
parser.add_argument('comment_id', type=str, required=False, help='Search all reports by comment_id.')
parser.add_argument('from_date', type=str, required=False, help='Search all reports by start created date.')
parser.add_argument('to_date', type=str, required=False, help='Search all reports by finish created date.')


@api.route('/search')
@api.expect(parser)
class VoteSearch(Resource):
    @token_required
    @api.response(code=200, model=report_response, description='The model for report response.')
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
        controller = ReportController()
        return controller.search(args=args)
