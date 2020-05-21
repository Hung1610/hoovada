from flask_restx import marshal

from app.modules.common.controller import Controller
from .topic import Topic
from .topic_dto import TopicDto
from ... import db
from ...utils.response import send_error, send_result


class TopicController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        if not 'name' in data:
            return send_error(message='Topic name must be filled')
        try:
            topic = Topic.query.filter_by(name=data['name']).first()
            if not topic:  # the topic does not exist
                topic = self._parse_topic(data=data, topic=None)
                db.session.add(topic)
                db.session.commit()
                return send_result(message='Topic was created successfully.', data=marshal(topic, TopicDto.model))
            else:  # topic already exist
                return send_error(message='The topic with name {} already exist'.format(data['name']))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Coult not create topic. Contact administrator for solution.')

    def get(self):
        try:
            topics = Topic.query.all()
            return send_result(data=marshal(topics, TopicDto.model), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load topics. Contact your administrator for solution.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Topic ID is null")
        topic = Topic.query.filter_by(topic_id=object_id).first()
        if topic is None:
            return send_error(message="Could not find topic by this ID {}".format(object_id))
        else:
            return send_result(data=marshal(topic, TopicDto.model), message='Success')

    def update(self, object_id, data):
        try:
            topic = Topic.query.filter_by(topic_id=object_id).first()
            if not topic:
                return send_error(message='Topic with the ID {} not found.'.format(object_id))
            else:
                topic = self._parse_topic(data=data, topic=topic)
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(topic, TopicDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update topic.')

    def delete(self, object_id):
        try:
            topic = Topic.query.filter_by(topic_id=object_id).first()
            if not topic:
                return send_error(message="Topic with ID {} not found".format(object_id))
            else:
                db.session.delete(topic)
                db.session.commit()
                return send_result(message='Topic was deleted.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user with ID {}'.format(object_id))

    def _parse_topic(self, data, topic=None):
        if topic is None:
            topic = Topic()
        if 'name' in data:
            topic.name = data['name']
        if 'count' in data:
            topic.count = int(data['count'])
        if 'user_id' in data:
            topic.user_id = int(data['user_id'])
        if 'question_count' in data:
            topic.question_count = int(data['question_count'])
        if 'user_count' in data:
            topic.user_count = int(data['user_count'])
        if 'answer_count' in data:
            topic.answer_count = int(data['answer_count'])
        return topic
