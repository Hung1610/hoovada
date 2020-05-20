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
        pass

    @api.expect(_user_topic)
    def post(self):
        pass


@api.route('/<int:user_topic_id>')
class UserTopic(Resource):
    @api.marshal_with(_user_topic)
    def get(self, user_topic_id):
        pass

    @api.expect(_user_topic)
    def post(self, user_topic_id):
        pass

    def delete(self, user_topic_id):
        pass
