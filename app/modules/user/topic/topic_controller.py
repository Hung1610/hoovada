#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.user.topic.topic_dto import TopicDto
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserTopic = db.get_model('UserTopic')
Topic = db.get_model('Topic')
TopicUserEndorse = db.get_model('TopicUserEndorse')
User = db.get_model('User')


class TopicController(Controller):

    def create(self, data,  user_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if user_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
        data['user_id'] = user_id

        try:
            topic = self._parse_topic(data=data, topic=None)
            db.session.add(topic)
            db.session.commit()
            return send_result( data=marshal(topic, TopicDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args, user_id=None):
        
        fixed_topic_id, topic_id, is_fixed = None, None, None
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
        if 'is_fixed' in args:
            try:
                is_fixed = args['is_fixed']
            except Exception as e:
                print(e.__str__())
                pass
        try:
            query = UserTopic.query

            query = query.join(User, isouter=True)\
                .filter((UserTopic.user == None) | (User.is_deactivated == False))

            if user_id is not None:
                query = query.filter(UserTopic.user_id == user_id)
            if fixed_topic_id is not None:
                query = query.filter(UserTopic.topic.parent_id == fixed_topic_id)
            if topic_id is not None:
                query = query.filter(UserTopic.topic_id == topic_id)
            if is_fixed is not None:
                query = query.filter(UserTopic.topic.is_fixed == True)
                
            topics = query.all()
            return send_result(data=marshal(topics, TopicDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self):
        pass


    def update(self, data, object_id):
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            topic = UserTopic.query.filter_by(id=object_id).first()
            if topic is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            topic = self._parse_topic(data=data, topic=topic)
            topic.updated_date = datetime.utcnow()
            db.session.commit()
            return send_result(data=marshal(topic, TopicDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))  

        try:
            topic = UserTopic.query.filter_by(id=object_id).first()
            if topic is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(topic)
            db.session.commit()
            return send_result()

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_endorsed_topics(self, args, user_id):
        
        if not 'page' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('page'))
        
        if not 'per_page' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('per_page'))

        page, per_page = args.get('page', 0), args.get('per_page', 10)
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return send_error(message=messages.ERR_NOT_FOUND)
                
            user_endorsed_topics = TopicUserEndorse.query.distinct()\
                .filter_by(endorsed_id=user.id)\
                .join(Topic, isouter=True)\
                .with_entities(
                    Topic,
                    db.func.count(TopicUserEndorse.user_id).label('endorse_score'),
                )\
                .group_by(Topic,)\
                .order_by(db.desc('endorse_score'))
            result = user_endorsed_topics.paginate(page, per_page, error_out=False)
            res, code = paginated_result(result)
            res['data'] = marshal([{'topic': topic, 'endorse_score': endorse_score} for topic, endorse_score in res.get('data')], TopicDto.model_endorsed_topic)
            return res, code
            
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


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
            try:
                topic.description = data['description']
            except Exception as e:
                print(e.__str__())
                pass

        if 'fixed_topic_id' in data:
            try:
                topic.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'topic_id' in data:
            try:
                topic.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_visible' in data:
            try:
                topic.is_visible = bool(data['is_visible'])
            except Exception as e:
                print(e.__str__())
                pass
                
        return topic
