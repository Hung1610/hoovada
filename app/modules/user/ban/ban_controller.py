#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

# built-in modules
import dateutil.parser
# third-party modules
from flask import current_app, request
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from common.db import db
from app.constants import messages
from app.modules.user.ban.ban_dto import UserBanDto
from common.controllers.controller import Controller
from common.models import User
from common.models.ban import BanTypeEnum, UserBan
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserBanController(Controller):
    def get(self, args):
        
        ban_by, \
        created_date, \
        expiry_date = \
            args.get('ban_by'), \
            args.get('created_date'), \
            args.get('expiry_date')

        query = UserBan.query
        if ban_by is not None:
            query = query.filter(UserBan.ban_by == ban_by)
        if created_date is not None:
            query = query.filter(UserBan.created_date <= created_date)
        if expiry_date is not None:
            query = query.filter(UserBan.expiry_date <= expiry_date)
        bans = query.all()
        if bans is not None and len(bans) > 0:
            return send_result(data=marshal(bans, UserBanDto.model_response), message='Success')
        else:
            return send_result(message=messages.ERR_NOT_FOUND)

    def create(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user, _ = current_app.get_logged_user(request)

        results = []
        try:
            data['ban_by'] = user.email
            data['user_id'] = current_user.id
            ban = UserBan.query.filter(UserBan.ban_by == data['ban_by']).first()
            if not ban:
                ban = self._parse_ban(data=data, ban=None)
                db.session.add(ban)
                db.session.commit()
                results.append(ban)

            data['ban_by'] = user.phone_number
            data['user_id'] = current_user.id
            ban = UserBan.query.filter(UserBan.ban_by == data['ban_by']).first()
            if not ban:
                ban = self._parse_ban(data=data, ban=None)
                db.session.add(ban)
                db.session.commit()
                results.append(ban)

            return send_result( data=marshal(results, UserBanDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
        ban = UserBan.query.filter_by(id=object_id).first()
        if ban is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Ban', object_id))
        else:
            return send_result(data=marshal(ban, UserBanDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        try:
            ban = UserBan.query.filter_by(id=object_id).first()
            if ban is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Ban', object_id))
            else:
                db.session.delete(ban)
                db.session.commit()
                return send_result()
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
    
    def _parse_ban(self, data, ban=None):
        if ban is None:
            ban = UserBan()
        if 'ban_by' in data:
            try:
                ban.ban_by = data['ban_by']
            except Exception as e:
                print(e.__str__())
                pass
        if 'ban_type' in data:
            try:
                ban_type = int(data['ban_type'])
                ban.ban_type = BanTypeEnum(ban_type).name
            except Exception as e:
                print(e.__str__())
                pass
        if 'expiry_date' in data:
            try:
                ban.expiry_date = data['expiry_date']
            except Exception as e:
                print(e)
                pass
        if 'user_id' in data:
            try:
                ban.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return ban