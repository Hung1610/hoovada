from app.modules.common.view import Resource
from .topic_dto import TopicDto
from .topic import Topic
from .topic_controller import TopicController

api = TopicDto.api
topic = TopicDto.model


@api.route('')
class UserTopicList(Resource):
    @api.marshal_list_with(topic)
    def get(self):
        pass

    @api.expect(topic)
    def post(self):
        pass


@api.route('/<int:topic_id>')
class UserTopic(Resource):
    @api.marshal_with(topic)
    def get(self, topic_id):
        pass

    @api.expect(topic)
    def post(self, topic_id):
        pass

    def delete(self, topic_id):
        pass
