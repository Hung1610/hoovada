from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .reporting_dto import ReportingDto
from .reporting_controller import ReportingController
from ...auth.decorator import admin_token_required, token_required

api = ReportingDto.api
reporting = ReportingDto.model


@api.route('')
class ReportingList(Resource):
    @admin_token_required
    @api.marshal_list_with(reporting)
    def get(self):
        '''
        Get list of reportings from database.

        :return: The list of reportings.
        '''
        controller = ReportingController()
        return controller.get()

    @token_required
    @api.expect(reporting)
    @api.marshal_with(reporting)
    def post(self):
        '''
        Create new reporting.

        :return: The new reporting if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = ReportingController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Reporting(Resource):
    @token_required
    @api.marshal_with(reporting)
    def get(self, id):
        '''
        Get reporting by its ID.

        :param id: The ID of the reporting.

        :return: The reporting with the specific ID.
        '''
        controller = ReportingController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(reporting)
    @api.marshal_with(reporting)
    def put(self, id):
        '''
        Update existing reporting by its ID.

        :param id: The ID of the reporting which need to be updated.

        :return: The updated reporting if success and null vice versa.
        '''
        data = api.payload
        controller = ReportingController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete reporting by its ID.

        :param id: The ID of the reporting.

        :return:
        '''
        controller = ReportingController()
        return controller.delete(object_id=id)
