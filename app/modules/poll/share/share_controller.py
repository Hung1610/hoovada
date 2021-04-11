#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal
from sqlalchemy import desc

# own modules
from common.db import db
from app.constants import messages
from app.modules.poll.share.share_dto import ShareDto
from common.controllers.controller import Controller
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Poll = db.get_model('Poll')
PollShare = db.get_model('PollShare')


class ShareController(Controller):
    def get(self, poll_id, args):
        user_id, from_date, to_date, facebook, twitter, zalo = None, None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                pass
        if 'from_date' in args:
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'facebook' in args and args['facebook'] is not None:
            try:
                facebook = bool(args['facebook'])
            except Exception as e:
                pass
        if 'twitter' in args and args['twitter'] is not None:
            try:
                twitter = bool(args['twitter'])
            except Exception as e:
                pass
        if 'zalo' in args and args['zalo'] is not None:
            try:
                zalo = bool(args['zalo'])
            except Exception as e:
                pass

        query = PollShare.query
        if user_id is not None:
            query = query.filter(PollShare.user_id == user_id)
        if poll_id is not None:
            query = query.filter(PollShare.poll_id == poll_id)
        if from_date is not None:
            query = query.filter(PollShare.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PollShare.created_date <= to_date)
        if facebook is not None:
            query = query.filter(PollShare.facebook == facebook)
        if twitter is not None:
            query = query.filter(PollShare.twitter == twitter)
        if zalo is not None:
            query = query.filter(PollShare.zalo == zalo)
        shares = query.all()
        if len(shares) > 0:
            return send_result(data=marshal(shares, ShareDto.model_response), message='Success')
        else:
            return send_result(messages.ERR_NOT_FOUND.format('Poll Share'))

    def create(self, poll_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        current_user, _ = current_app.get_logged_user(request)
        if not has_permission(current_user.id, PermissionType.SHARE):
            return send_error(code=401, message='You have no authority to perform this action')

        data['user_id'] = current_user.id
        data['poll_id'] = poll_id
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                poll = Poll.query.filter_by(id=share.poll_id).first()
                if not poll:
                    return send_error(message=messages.ERR_NOT_FOUND.format('Poll'))
                user_shared = User.query.filter_by(id=poll.user_id).first()
                if not user_shared:
                    return send_error(message=messages.ERR_NOT_FOUND.format('User'))
                user_shared.poll_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.poll_share_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result(data=marshal(share, ShareDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Poll Share', e))

    def get_by_id(self, object_id):
        query = PollShare.query
        share = query.filter(PollShare.id == object_id).first()
        if share is None:
            return send_error(message=messages.ERR_NOT_FOUND.format('Poll Share'))
        else:
            return send_result(data=marshal(share, ShareDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data):
        share = PollShare()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'poll_id' in data:
            try:
                share.poll_id = int(data['poll_id'])
            except Exception as e:
                pass
        if 'facebook' in data:
            try:
                share.facebook = bool(data['facebook'])
            except Exception as e:
                pass
        if 'twitter' in data:
            try:
                share.twitter = bool(data['twitter'])
            except Exception as e:
                pass
        if 'linkedin' in data:
            try:
                share.linkedin = bool(data['linkedin'])
            except Exception as e:
                pass
        if 'zalo' in data:
            try:
                share.zalo = bool(data['zalo'])
            except Exception as e:
                pass
        if 'vkontakte' in data:
            try:
                share.vkontakte = bool(data['vkontakte'])
            except Exception as e:
                pass
        if 'mail' in data:
            try:
                share.mail = bool(data['mail'])
            except Exception as e:
                pass
        if 'link_copied' in data:
            try:
                share.link_copied = bool(data['link_copied'])
            except Exception as e:
                pass
        return share
