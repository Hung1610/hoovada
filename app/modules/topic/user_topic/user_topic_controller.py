from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.topic.user_topic.user_topic import UserTopic
from app.modules.topic.user_topic.user_topic_dto import UserTopicDto
from app.utils.response import send_error, send_result


class UserTopicController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary type.')
        try:
            user_id = data['user_id']
            topic_id = data['topic_id']
            user_topic = UserTopic.query.filter(UserTopic.user_id == user_id, UserTopic.topic_id == topic_id).first()
            if user_topic is not None:
                return send_error(
                    message='This user with ID {} already follow this topic with ID {}'.format(user_id, topic_id))
            else:
                db.session.add(user_topic)
                db.session.commit()
                return send_result(data=marshal(user_topic, UserTopicDto.model), message='Create successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e.__str__())

    def get(self):
        try:
            user_topics = UserTopic.query.all()
            return send_result(data=marshal(user_topics, UserTopicDto.model), message='Success.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get list of user-topics.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error('User-topic ID is null')
        user_topic = UserTopic.query.filter_by(id=object_id).first()
        if user_topic is None:
            return send_error(message='Could not find user-topic with the ID {}'.format(object_id))
        else:
            return send_result(data=marshal(user_topic, UserTopicDto.model), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error('User-topic ID is null')
        try:
            user_topic = UserTopic.query.filter_by(id=object_id).first()
            if user_topic is None:
                return send_error(message='User topic with the ID {} not found'.format(object_id))
            else:
                user_topic = self._parse_user_topic(data=data, user_topic=user_topic)
                db.session.commit()
                return send_result(data=marshal(user_topic, UserTopicDto.model), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update user-topic')

    def delete(self, object_id):
        if object_id is None:
            return send_error('User-topic ID is null')
        try:
            user_topic = UserTopic.query.filter_by(id=object_id).first()
            if user_topic is None:
                return send_error(message='User-topic with the ID {} not found.'.format(object_id))
            else:
                db.session.delete(user_topic)
                db.session.commit()
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user-topic with ID {}'.format(object_id))

    def _parse_user_topic(self, data, user_topic=None):
        if user_topic is None:
            user_topic = UserTopic()
        if 'user_id' in data:
            try:
                user_topic.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in data:
            try:
                user_topic.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return user_topic
