#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime, timedelta

# third-party modules
from flask import current_app, request
from flask_restx import marshal

# own modules
from common.db import db
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

    def get_by_id(self, object_id):
        raise NotImplementedError()


    def update(self, object_id):
        raise NotImplementedError()


    def get(self, poll_select_id, args):
        current_user, _ = current_app.get_logged_user(request)
        poll_user_selects = PollUserSelect.query.filter_by(poll_select_id=poll_select_id).all()
        if poll_user_selects is None or len(poll_user_selects) == 0:
            return send_result(message='Could not find any poll user select.')
        return send_result(marshal(poll_user_selects, PollUserSelectDto.model_response), message='Success')


    def delete(self, object_id):
        try:
            current_user, _ = current_app.get_logged_user(request)    
            poll_user_select = PollUserSelect.query.filter_by(id=object_id).first()
            if poll_user_select is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll User Select', object_id))            
            if poll_user_select.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            db.session.delete(poll_user_select)
            db.session.commit()
            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Poll User Topic', e))


    def create(self, data):

        current_user, _ = current_app.get_logged_user(request)    
        if 'poll_select_id' not in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll_select_id'))

        poll_select_id = data['poll_select_id']

        poll_select = PollSelect.query.filter_by(id=poll_select_id).first()
        if poll_select is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Poll Select', poll_select_id))

        allow_multiple_user_select = poll_select.poll.allow_multiple_user_select
        
        if allow_multiple_user_select is False:
            poll_user_selects = PollUserSelect.query.filter_by(user_id=current_user.id).join(PollSelect).filter_by(poll_id=poll_select.poll.id).all()
            if len(poll_user_selects) > 0:
                return send_error(message=messages.ERR_ISSUE.format('You are not allowed to choose multiple options'))
        if poll_select.poll.expire_after_seconds is not None:
            past = datetime.utcnow() - timedelta(seconds=poll_select.poll.expire_after_seconds)
            if past > poll_select.poll.created_date:
                return send_error(message=messages.ERR_ISSUE.format('Poll already expired'))
        try:
            poll_user_select = PollUserSelect.query.filter_by(user_id=current_user.id, poll_select_id=poll_select_id).first()
            if poll_user_select is None or len(poll_user_select) == 0:
                data = {}
                data['poll_select_id'] = poll_select_id
                data['user_id'] = current_user.id
                poll_user_select = PollUserSelect()
                poll_user_select.poll_select_id = data['poll_select_id']
                poll_user_select.user_id = int(data['user_id'])
                poll_user_select.created_date = datetime.utcnow()
                poll_user_select.updated_date = datetime.utcnow()
                db.session.add(poll_user_select)
                db.session.commit()

            result = poll_user_select._asdict()
            return send_result( data=marshal(result, PollUserSelectDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
