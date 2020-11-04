#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal

# own modules
from app.app import db
from app.modules.topic.user_topic.user_topic import UserTopic
from app.modules.topic.user_topic.user_topic_dto import UserTopicDto
from common.controllers.controller import Controller
from common.models import Topic, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserTopicController(Controller):
    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Could not parse your parameters.')
        user_id, topic_id = None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in args:
            try:
                topic_id = int(args['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if user_id is None and topic_id is None:
            return send_error(message='Please provide params to search')
        query = db.session.query(UserTopic)
        is_filter = False
        if user_id is not None:
            query = query.filter(UserTopic.user_id == user_id)
            is_filter = True
        if topic_id is not None:
            query = query.filter(UserTopic.topic_id == topic_id)
            is_filter = True
        if is_filter:
            question_topics = query.all()
            if question_topics is not None and len(question_topics) > 0:
                results = list()
                for question_topic in question_topics:
                    # get topics infor
                    topic_id = question_topic.topic_id
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                    result['topics'] = topics
                    results.append(result)
                return send_result(marshal(results, UserTopicDto.model_response), message='Success')
            else:
                return send_result(message='Not found.', code=201)
        else:
            return send_error(message='Could not find any records.')

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
                # create user_topic
                user_topic = self._parse_user_topic(data=data, user_topic=None)
                user_topic.created_date = datetime.utcnow()
                db.session.add(user_topic)
                db.session.commit()
                # update user_count for topic and topic_followed_count for table user
                try:
                    # get topic
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topic.user_count += 1  # update user_count
                    # get user who created this topic
                    user = User.query.filter_by(id=topic.user_id).first()
                    user.topic_followed_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                    pass
                # update topic_follow_count for table user
                try:
                    user = User.query.filter_by(id=user_id).first()
                    user.topic_follow_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                    pass
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
                return send_result(message='Deleted successfully.')
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
