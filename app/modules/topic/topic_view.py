from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .topic_dto import TopicDto
from .topic_controller import TopicController
from ..auth.decorator import admin_token_required, token_required

api = TopicDto.api
topic = TopicDto.model


@api.route('')
class TopicList(Resource):
    @admin_token_required
    @api.marshal_list_with(topic)
    def get(self):
        '''
        Get list of topics from database.

        :return: The list of topics.
        '''
        controller = TopicController()
        return controller.get()

    @token_required
    @api.expect(topic)
    @api.marshal_with(topic)
    def post(self):
        '''
        Create new topic.

        :return: The new topic if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = TopicController()
        return controller.create(data=data)


@api.route('/<int:topic_id>')
class Topic(Resource):
    @token_required
    @api.marshal_with(topic)
    def get(self, topic_id):
        '''
        Get topic by its ID.

        :param topic_id: The ID of the topic.

        :return: The topic with the specific ID.
        '''
        controller = TopicController()
        return controller.get_by_id(object_id=topic_id)

    @token_required
    @api.expect(topic)
    @api.marshal_with(topic)
    def put(self, topic_id):
        '''
        Update existing topic by its ID.

        :param topic_id: The ID of the topic which need to be updated.

        :return: The updated topic if success and null vice versa.
        '''
        data = api.payload
        controller = TopicController()
        return controller.update(object_id=topic_id, data=data)

    @token_required
    def delete(self, topic_id):
        '''
        Delete topic by its ID.

        :param topic_id: The ID of the topic.

        :return:
        '''
        controller = TopicController()
        return controller.delete(object_id=topic_id)
