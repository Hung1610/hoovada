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
from app.modules.poll.poll_select.poll_select_dto import PollSelectDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Poll = db.get_model('Poll')
PollTopic = db.get_model('PollTopic')
PollSelect = db.get_model('PollSelect')
PollUserSelect = db.get_model('PollUserSelect')
User = db.get_model('User')

class PollSelectController(Controller):
    query_classname = 'PollSelect'

    def _parse_poll_select(self, data, poll_select=None):
        if poll_select is None:
            poll_select = PollSelect()
        if 'content' in data:
            try:
                poll_select.content = data['content']
            except Exception as e:
                print(e.__str__())
                pass
        if 'poll_id' in data:
            poll_select.poll_id = int(data['poll_id'])
        return poll_select
    
    def get_by_id(self, object_id):
        raise NotImplementedError()

    def get(self, poll_id, args):
        try:
            if not poll_id:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll id'))

            poll_id = int(poll_id)
            poll_selects = PollSelect.query.filter_by(poll_id=poll_id).all()
            if poll_selects is None or len(poll_selects) == 0:
                return send_result(message='Could not find any poll selects.')
            
            return send_result(marshal(poll_selects, PollSelectDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('Poll Select', e))

    def delete(self, object_id):
        try:
            poll_select = PollSelect.query.filter_by(id=object_id).first()
            if poll_select is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user, _ = current_app.get_logged_user(request)
            if poll_select.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(poll_select)
            db.session.commit()
            return send_result()
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))

    def create(self, data, poll_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        if not 'content' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll select content'))
        if not poll_id:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll id'))

        current_user, _ = current_app.get_logged_user(request)

        poll = Poll.query.filter_by(id=poll_id).first()
        if poll is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', poll_id))
        
        if poll.user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        data['user_id'] = current_user.id
        data['poll_id'] = poll_id
        try:
            poll_select = self._parse_poll_select(data=data, poll_select=None)
            if poll_select.content.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll_select content'))
            poll_select.created_date = datetime.utcnow()
            poll_select.updated_date = datetime.utcnow()
            poll_select.user_id = data['user_id']
            db.session.add(poll_select)
            db.session.commit()
            result = poll_select._asdict()
            return send_result( data=marshal(result, PollSelectDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def update(self, object_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'content' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll select content'))

        current_user, _ = current_app.get_logged_user(request)
        try:
            poll_select = PollSelect.query.filter_by(id=object_id).first()
            if poll_select is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Select', object_id))
            poll = Poll.query.filter_by(id=poll_select.poll_id).first()
            if poll is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll', poll_select.poll_id))
            
            if poll.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            
            poll_select = self._parse_poll_select(data=data, poll_select=poll_select)
            if poll_select.content.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll_select content'))
            poll_select.updated_date = datetime.utcnow()
            db.session.commit()
            result = poll_select._asdict()
            return send_result(data=marshal(result, PollSelectDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))
