from app.modules.common.view import Resource
from .topic_dto import TopicDto
from .topic import Topic
from .topic_controller import TopicController

api = TopicDto.api
topic = TopicDto.model


@api.route('')
class TopicList(Resource):
    @api.marshal_list_with(topic)
    def get(self):
        """
        Get list of topics in database.

        This function only done with user who has admin right.

        :return: List of topics and sub-topics.
        """
        controller = TopicController()
        return controller.get()

    @api.expect(topic)
    @api.marshal_with(topic)
    def post(self):
        """
        Create Topic

        :return:
        """
        data = api.payload
        controller = TopicController()
        return controller.create(data=data)


@api.route('/<int:topic_id>')
class Topic(Resource):
    @api.marshal_with(topic)
    def get(self, topic_id):
        """
        Get topic in database using it ID.

        :param topic_id: The ID of the topic

        :return: The topic.
        """
        controller = TopicController()
        return controller.get_by_id(object_id=topic_id)

    @api.expect(topic)
    def put(self, topic_id):
        """
        Update topic in database.
        ------------------

        :param topic_id: The ID of the topic.

        """
        data = api.payload
        controller = TopicController()
        return controller.update(object_id=topic_id, data=data)

    def delete(self, topic_id):
        """
        Delete the topic by its ID.

        :param topic_id:

        :return:

        """
        controller = TopicController()
        return controller.delete(object_id=topic_id)
