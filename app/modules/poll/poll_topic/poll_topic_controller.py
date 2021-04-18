#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from flask import current_app, request
# third-party modules
from flask_restx import marshal

# own modules
from common.db import db
from common.utils.response import send_error, send_result
from common.controllers.controller import Controller
from app.constants import messages
from app.modules.poll.poll_topic.poll_topic_dto import PollTopicDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Poll = db.get_model('Poll')
PollTopic = db.get_model('PollTopic')
PollUserSelect = db.get_model('PollUserSelect')
User = db.get_model('User')

class PollTopicController(Controller):
    query_classname = 'PollTopic'

    def _parse_poll_topic(self, data, poll_topic=None):
        if poll_topic is None:
            poll_topic = PollTopic()
        if 'topic_id' in data:
            try:
                poll_topic.topic_id = data['topic_id']
            except Exception as e:
                print(e.__str__())
                pass
        if 'poll_id' in data:
            poll_topic.poll_id = int(data['poll_id'])
        return poll_topic
    
    def get_by_id(self, object_id):
        raise NotImplementedError()

    def get(self, poll_id, args):
        try:
            if not poll_id:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll id'))
            poll_id = int(poll_id)
            poll_topics = PollTopic.query.filter_by(poll_id=poll_id).all()
            if poll_topics is None or len(poll_topics) == 0:
                return send_result(message='Could not find any poll topics.')
            return send_result(marshal(poll_topics, PollTopicDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('Poll Topic', e))

    def delete(self, object_id):
        try:
            poll_topic = PollTopic.query.filter_by(id=object_id).first()
            if poll_topic is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Topic', object_id))

            current_user, _ = current_app.get_logged_user(request)
            if current_user is None or (poll_topic.user_id != current_user.id):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(poll_topic)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Poll Topic', e))

    def create(self, data, poll_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        if not 'topic_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll topic content'))
        if not poll_id:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll id'))
        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_LOGIN)
        poll = Poll.query.filter_by(id=poll_id).first()
        if poll is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', poll_id))
        if poll.user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        existing_poll_topics = PollTopic.query.filter_by(poll_id=poll_id, topic_id=data['topic_id']).all()
        if existing_poll_topics is not None and len(existing_poll_topics) != 0:
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll Topic', 'This poll topic has already existed!'), data={'poll_id': int(poll_id), 'topic_id': int(data['topic_id'])})
        try:
            data['poll_id'] = poll_id
            poll_topic = self._parse_poll_topic(data=data, poll_topic=None)
            poll_topic.created_date = datetime.utcnow()
            poll_topic.updated_date = datetime.utcnow()
            db.session.add(poll_topic)
            db.session.commit()
            result = poll_topic._asdict()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Poll Topic'), data=marshal(result, PollTopicDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll', str(e)))

    def update(self, object_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        if not 'content' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll topic content'))

        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_LOGIN)
        try:
            poll_topic = PollTopic.query.filter_by(id=object_id).first()
            if poll_topic is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Topic', object_id))
            poll = poll_topic.poll
            if poll is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', poll_topic.poll_id))
            if poll.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            poll_topic = self._parse_poll_topic(data=data, poll_topic=poll_topic)
            if poll_topic.content.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll_topic content'))
            poll_topic.updated_date = datetime.utcnow()
            db.session.commit()
            result = poll_topic._asdict()
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('PollTopic'), data=marshal(result, PollTopicDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format('PollTopic', str(e)))
