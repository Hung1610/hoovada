from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .timeline_dto import TimelineDto
from .timeline_controller import TimelineController
from ...auth.decorator import admin_token_required, token_required

api = TimelineDto.api
timeline = TimelineDto.model


@api.route('')
class TimelineList(Resource):
    @admin_token_required
    @api.marshal_list_with(timeline)
    def get(self):
        '''
        Get list of timelines from database.

        :return: The list of timelines.
        '''
        controller = TimelineController()
        return controller.get()

    @token_required
    @api.expect(timeline)
    @api.marshal_with(timeline)
    def post(self):
        '''
        Create new timeline.

        :return: The new timeline if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = TimelineController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Timeline(Resource):
    @token_required
    @api.marshal_with(timeline)
    def get(self, id):
        '''
        Get timeline by its ID.

        :param id: The ID of the timeline.

        :return: The timeline with the specific ID.
        '''
        controller = TimelineController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(timeline)
    @api.marshal_with(timeline)
    def put(self, id):
        '''
        Update existing timeline by its ID.

        :param id: The ID of the timeline which need to be updated.

        :return: The updated timeline if success and null vice versa.
        '''
        data = api.payload
        controller = TimelineController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete timeline by its ID.

        :param id: The ID of the timeline.

        :return:
        '''
        controller = TimelineController()
        return controller.delete(object_id=id)
