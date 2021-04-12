#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from flask import current_app, request
# third-party modules
from flask_restx import marshal

# own modules
from common.db import db
from common.utils.onesignal_notif import push_notif_to_specific_users
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.controllers.controller import Controller
from app.constants import messages
from app.modules.poll.poll_user_select.poll_user_select_dto import PollUserSelectDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Poll = db.get_model('Poll')
PollSelect = db.get_model('PollSelect')
PollUserSelect = db.get_model('PollUserSelect')
User = db.get_model('User')

class PollUserSelectController(Controller):
    query_classname = 'PollUserSelect'

    def _auth_poll_select(self, poll_select_id, current_user):
        poll_select = PollSelect.query.filter_by(id=poll_select_id).first()
        if poll_select is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Select', poll_select_id))
        if poll_select.created_by_user_id!= current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

    def _auth_poll_user_select(self, poll_user_select_id, current_user):
        poll_user_select = PollUserSelect.query.filter_by(id=poll_user_select_id).first()
        if poll_user_select is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll User Select', poll_user_select_id))
        if poll_user_select.poll_select is None:
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll Select', 'This poll select has been deleted!'))
        if poll_user_select.poll_select.created_by_user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

    def _parse_poll_user_select(self, data, poll_user_select=None):
        if poll_user_select is None:
            poll_user_select = PollUserSelect()
        if 'poll_select_id' in data:
            try:
                poll_user_select.poll_select_id = data['poll_select_id']
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            poll_user_select.user_id = int(data['user_id'])
        return poll_user_select
    
    def get_by_id(self, object_id):
        raise NotImplementedError()

    def update(self, object_id):
        raise NotImplementedError()

    def get(self, poll_select_id, args):
        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_LOGIN)
        self._auth_poll_select(poll_select_id=poll_select_id, current_user=current_user)
        poll_user_selects = PollUserSelect.query.filter_by(poll_select_id=poll_select_id)
        if poll_user_selects is None or len(poll_user_selects) == 0:
            return send_result(message='Could not find any poll user select.')
        return send_result(marshal(poll_user_selects, PollUserSelect.model_response), message='Success')
    def delete(self, object_id):
        try:
            current_user, _ = current_app.get_logged_user(request)
            if not current_user:
                return send_error(code=401, message=messages.ERR_NOT_LOGIN)
            self._auth_poll_user_select(poll_user_select_id=object_id, current_user=current_user)
            poll_user_select = PollUserSelect.query.filter_by(id=object_id).first()
            if poll_user_select is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll User Select', object_id))            
            db.session.delete(poll_user_select)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Poll User Topic', e))

    def create(self, poll_select_id):
        if not poll_select_id:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll user select id'))
        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_LOGIN)
        self._auth_poll_select(poll_select_id=poll_select_id, current_user=current_user)
        existing_poll_user_selects = PollUserSelect.query.filter_by(user_id=current_user.id, poll_select_id=poll_select_id).all()
        if existing_poll_user_selects is not None and len(existing_poll_user_selects) != 0:
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll User Select', 'This poll user select has already existed!'), data={'poll_select_id': int(poll_select_id), 'user_id': int(current_user.id)})
        poll_select = PollSelect.query.filter_by(id=poll_select_id).first()
        if not poll_select:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Select', poll_select_id))
        if not poll_select.poll:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll'))
        allow_multiple_user_select = poll_select.poll.allow_multiple_user_select
        if allow_multiple_user_select is False:
            poll_user_selects = PollUserSelect.query.filter_by(user_id=current_user.id).join(PollSelect).filter_by(poll_id=poll_select.poll.id).all()
            if len(poll_user_selects) > 0:
                return send_error(message=messages.ERR_ISSUE.format('You are not allowed to choose multiple options'))
        try:
            data = {}
            data['poll_select_id'] = poll_select_id
            data['user_id'] = current_user.id
            poll_user_select = self._parse_poll_user_select(data=data, poll_user_select=None)
            poll_user_select.created_date = datetime.utcnow()
            poll_user_select.updated_date = datetime.utcnow()
            db.session.add(poll_user_select)
            db.session.commit()
            result = poll_user_select._asdict()
            print('--resultssss', result)
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Poll User Select'), data=marshal(result, PollUserSelectDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll User Select', str(e)))
