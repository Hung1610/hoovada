#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask_restx import marshal
from flask import request
from sqlalchemy import desc

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.answer.share.share import AnswerShare
from app.modules.q_a.answer.share.share_dto import AnswerShareDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.modules.auth.auth_controller import AuthController
from app.utils.types import UserRole, PermissionType
from app.utils.permission import has_permission
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ShareController(Controller):
    def get(self, answer_id, args):
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
        if 'facebook' in args:
            try:
                facebook = bool(args['facebook'])
            except Exception as e:
                pass
        if 'twitter' in args:
            try:
                twitter = bool(args['twitter'])
            except Exception as e:
                pass
        if 'zalo' in args:
            try:
                zalo = bool(args['zalo'])
            except Exception as e:
                pass

        query = AnswerShare.query
        if user_id is not None:
            query = query.filter(AnswerShare.user_id == user_id)
        if answer_id is not None:
            query = query.filter(AnswerShare.answer_id == answer_id)
        if from_date is not None:
            query = query.filter(AnswerShare.created_date >= from_date)
        if to_date is not None:
            query = query.filter(AnswerShare.created_date <= to_date)
        if facebook is not None:
            query = query.filter(AnswerShare.facebook == facebook)
        if twitter is not None:
            query = query.filter(AnswerShare.twitter == twitter)
        if zalo is not None:
            query = query.filter(AnswerShare.zalo == zalo)
        shares = query.all()
        if len(shares) > 0:
            return send_result(data=marshal(shares, AnswerShareDto.model_response), message='Success')
        else:
            return send_result('Answer shares not found.')

    def create(self, answer_id, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not in the correct format')
        current_user, _ = AuthController.get_logged_user(request)
        # Check is admin or has permission
        if not (UserRole.is_admin(current_user.admin)
                or has_permission(current_user.id, PermissionType.ANSWER_SHARE)):
            return send_error(code=401, message=messages.MSG_NOT_DO_ACTION)

        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                answer = Answer.query.filter_by(id=share.answer_id).first()
                if not answer:
                    return send_error(message='Answer not found.')
                user_voted = User.query.filter_by(id=answer.user_id).first()
                if not user_voted:
                    return send_error(message='User not found.')
                user_voted.answer_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.answer_share_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result(data=marshal(share, AnswerShareDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to create answer share.')

    def get_by_id(self, object_id):
        query = AnswerShare.query
        report = query.filter(AnswerShare.id == object_id).first()
        if report is None:
            return send_error(message='Answer share not found.')
        else:
            return send_result(data=marshal(report, AnswerShareDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data):
        share = AnswerShare()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'answer_id' in data:
            try:
                share.answer_id = int(data['answer_id'])
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
