#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from flask import current_app, request
# third-party modules
from flask_restx import marshal

# own modules
from common.db import db
from common.utils.response import send_error, send_result, paginated_result
from common.controllers.controller import Controller
from app.constants import messages
from app.modules.poll.poll_dto import PollDto
from common.dramatiq_producers import update_seen_poll

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Poll = db.get_model('Poll')
PollTopic = db.get_model('PollTopic')
PollSelect = db.get_model('PollSelect')
PollUserSelect = db.get_model('PollUserSelect')
User = db.get_model('User')
Post = db.get_model('Post')

class PollController(Controller):
    query_classname = 'Poll'

    def _parse_poll(self, data, poll=None):
        if poll is None:
            poll = Poll()
        if 'title' in data:
            try:
                poll.title = data['title']
            except Exception as e:
                print(e.__str__())
                pass
        if 'allow_multiple_user_select' in data:
            poll.allow_multiple_user_select = bool(data['allow_multiple_user_select'])
        if 'owner_user_id' in data:
            try:
                poll.owner_user_id = int(data['owner_user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'expire_after_seconds' in data:
            try:
                poll.expire_after_seconds = data['expire_after_seconds']
            except Exception as e:
                print(e.__str__())
                pass
        return poll

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            results = []
            if res['data'] is not None:
                for poll in res['data']:
                    if poll:
                        results.append(poll._asdict())
            res['data'] = marshal(results, PollDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('Answer', e))
    
    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Poll ID"))
        poll = Poll.query.filter_by(id=object_id).first()
        current_user, _ = current_app.get_logged_user(request)
        if current_user is None:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        if poll is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', object_id))
        else:
            result = poll._asdict()
            result['own_user'] = poll.own_user
            result['topics'] = poll.topics
            result['poll_selects'] = poll.poll_selects
            update_seen_poll.send(current_user.id, poll.id)
            return send_result(data=marshal(result, PollDto.model_response))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Poll ID"))

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        try:
            poll = Poll.query.filter_by(id=object_id).first()
            if poll is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', object_id))
            current_user, _ = current_app.get_logged_user(request)
            if current_user is None or (poll.owner_user_id != current_user.id):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            poll = self._parse_poll(data=data, poll=poll)
            if poll.title.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll title'))
            poll.updated_date = datetime.utcnow()
            db.session.commit()
            result = poll._asdict()
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Poll'), data=marshal(result, PollDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format('Poll', e))


    def delete(self, object_id):
        try:
            poll = Poll.query.filter_by(id=object_id).first()
            if poll is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', object_id))

            current_user, _ = current_app.get_logged_user(request)
            if current_user is None or (poll.owner_user_id != current_user.id):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(poll)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Poll', e))

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        if not 'title' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll title'))
        if not 'allow_multiple_user_select' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll allow_multiple_user_select'))

        if not 'expire_after_seconds' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll expire_after_seconds'))

        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_LOGIN)

        data['owner_user_id'] = current_user.id
        try:
            poll = self._parse_poll(data=data, poll=None)
            if poll.title.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll title'))
            poll.created_date = datetime.utcnow()
            poll.updated_date = datetime.utcnow()
            poll.is_expire = False
            db.session.add(poll)
            db.session.commit()
            result = poll._asdict()
            update_seen_poll.send(current_user.id, poll.id)
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Poll'), data=marshal(result, PollDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll', str(e)))