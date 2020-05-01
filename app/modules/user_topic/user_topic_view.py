from app.modules.common.view import Resource
from app.modules.user_topic.user_topic_dto import UserTopicDto

api = UserTopicDto.api
_user_topic = UserTopicDto.model


@api.route('')
class UserTopicList(Resource):
    def get(self):
        pass

    def post(self):
        pass


@api.route('/<int:user_topic_id>')
class UserTopic(Resource):
    def get(self, user_topic_id):
        pass

    def post(self, user_topic_id):
        pass

    def delete(self, user_topic_id):
        pass
