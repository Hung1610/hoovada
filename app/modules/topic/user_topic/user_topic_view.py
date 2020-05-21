from app.modules.common.view import Resource
from .user_topic_dto import UserTopicDto
from .user_topic import UserTopic
from .user_topic_controller import UserTopicController

api = UserTopicDto.api
_user_topic = UserTopicDto.model


@api.route('')
class UserTopicList(Resource):
    @api.marshal_list_with(_user_topic)
    def get(self):
        """
        Get list of User topic mapping in the database.

        :return:
        """
        controller = UserTopicController()
        return controller.get()

    @api.expect(_user_topic)
    def post(self):
        """
        Create user-topic mapping.

        :return:
        """
        data = api.payload
        controller = UserTopicController()
        return controller.create(data=data)


@api.route('/<int:user_topic_id>')
class UserTopic(Resource):
    @api.marshal_with(_user_topic)
    def get(self, user_topic_id):
        """
        Get user-topic information by using its ID.
        -------------------------

        :param user_topic_id: The ID of the user-topic mapping.

        :return:
        """
        controller = UserTopicController()
        return controller.get_by_id(object_id=user_topic_id)

    @api.expect(_user_topic)
    def put(self, user_topic_id):
        """
        Update user-topic.
        ---------------

        :param user_topic_id: The ID of the user-topic mapping.

        :return:
        """
        data = api.payload
        controller = UserTopicController()
        return controller.update(object_id=user_topic_id, data=data)

    def delete(self, user_topic_id):
        """
        Delete user-topic mapping by using its ID.

        :param user_topic_id: The ID of the user-topic.

        :return:
        """
        controller = UserTopicController()
        return controller.delete(object_id=user_topic_id)
