#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal
from flask import request

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.topic.topic import Topic, TopicUserEndorse
from app.modules.user.user import User
from app.modules.user.topic.topic import UserTopic
from app.modules.user.topic.topic_dto import TopicDto
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.utils.response import send_error, send_result, send_paginated_result, paginated_result
from app.utils.sensitive_words import check_sensitive
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicController(Controller):
    def get(self, args, user_id=None):
        """
        Search topics by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        fixed_topic_id, topic_id = None, None
        if 'fixed_topic_id' in args:
            try:
                fixed_topic_id = int(args['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in args:
            try:
                topic_id = int(args['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = UserTopic.query
        if user_id is not None:
            query = query.filter(UserTopic.user_id == user_id)
        if fixed_topic_id is not None:
            query = query.filter(UserTopic.topic.parent_id == fixed_topic_id)
        if topic_id is not None:
            query = query.filter(UserTopic.topic_id == topic_id)
            
        topics = query.all()
        return send_result(marshal(topics, TopicDto.model_response), message='Success')

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('UserTopic ID is null')
            topic = UserTopic.query.filter_by(id=object_id).first()
            if topic is None:
                return send_error(message='Could not find topic with the ID {}'.format(object_id))
            return send_result(data=marshal(topic, TopicDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get topic with the ID {}'.format(object_id))

    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")

        data['user_id'] = user_id

        try:
            topic = self._parse_topic(data=data, topic=None)
            if topic.is_default:
                UserTopic.query.filter_by(user_id=user_id).update({'is_default': False}, synchronize_session=False)
            db.session.add(topic)
            db.session.commit()
            return send_result(data=marshal(topic, TopicDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not create topic. Error: ' + e.__str__())

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='UserTopic ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            topic = UserTopic.query.filter_by(id=object_id).first()
            if topic is None:
                return send_error(message='UserTopic with the ID {} not found.'.format(object_id))

            topic = self._parse_topic(data=data, topic=topic)
            topic.updated_date = datetime.utcnow()
            if topic.is_default:
                UserTopic.query.filter(UserTopic.id != topic.id, UserTopic.user_id == topic.user_id).update({'is_default': False}, synchronize_session=False)
            db.session.commit()
            return send_result(message='Update successfully', data=marshal(topic, TopicDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update topic. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            topic = UserTopic.query.filter_by(id=object_id).first()
            if topic is None:
                return send_error(message='UserTopic with the ID {} not found.'.format(object_id))
            db.session.delete(topic)
            db.session.commit()
            return send_result(message='UserTopic with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete topic with the ID {}.'.format(object_id))

    def get_endorsed_topics(self, user_id, args):
        if not 'page' in args:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('page'))
        if not 'per_page' in args:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('per_page'))
        page, per_page = args.get('page', 0), args.get('per_page', 10)
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('User', user_id))
            user_endorsed_topics = TopicUserEndorse.query.distinct()\
                .filter_by(endorsed_id=user.id)\
                .join(Topic, isouter=True)\
                .with_entities(
                    Topic,
                    db.func.count(TopicUserEndorse.user_id).label('endorse_score'),
                )\
                .group_by(Topic,)\
                .order_by(db.desc('endorse_score'))
            result = user_endorsed_topics.paginate(page, per_page, error_out=True)
            res, code = paginated_result(result)
            res['data'] = marshal([{'topic': topic, 'endorse_score': endorse_score} for topic, endorse_score in res.get('data')], TopicDto.model_endorsed_topic)
            return res, code
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_GET_FAILED.format('endorsed topics', e.__str__))

    def _parse_topic(self, data, topic=None):
        if topic is None:
            topic = UserTopic()
        if 'user_id' in data:
            try:
                topic.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'description' in data:
            topic.description = data['description']
        if 'fixed_topic_id' in data:
            try:
                topic.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e)
                pass
        if 'topic_id' in data:
            try:
                topic.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e)
                pass
        if 'is_default' in data:
            try:
                topic.is_default = bool(data['is_default'])
            except Exception as e:
                print(e.__str__())
                pass
        return topic
