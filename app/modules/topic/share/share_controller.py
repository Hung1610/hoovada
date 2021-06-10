#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.modules.topic.share.share_dto import TopicShareDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Topic = db.get_model('Topic')
User = db.get_model('User')
TopicShare = db.get_model('TopicShare')


class ShareController(Controller):
    def get(self, topic_id, args):
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

        try:
            query = TopicShare.query
            if user_id is not None:
                query = query.filter(TopicShare.user_id == user_id)
            if topic_id is not None:
                query = query.filter(TopicShare.topic_id == topic_id)
            if from_date is not None:
                query = query.filter(TopicShare.created_date >= from_date)
            if to_date is not None:
                query = query.filter(TopicShare.created_date <= to_date)
            if facebook is not None:
                query = query.filter(TopicShare.facebook == facebook)
            if twitter is not None:
                query = query.filter(TopicShare.twitter == twitter)
            if zalo is not None:
                query = query.filter(TopicShare.zalo == zalo)
            shares = query.all()
            return send_result(data=marshal(shares, TopicShareDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, topic_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        current_user = g.current_user

        data['user_id'] = current_user.id
        data['topic_id'] = topic_id
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                topic = Topic.query.filter_by(id=share.topic_id).first()
                if not topic:
                    return send_error(message='Topic not found.')
                user_voted = User.query.filter_by(id=topic.user_id).first()
                if not user_voted:
                    return send_error(message='User not found.')
                user_voted.topic_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.topic_share_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result()
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        try:
            query = TopicShare.query
            report = query.filter(TopicShare.id == object_id).first()
            if report is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                return send_result(data=marshal(report, TopicShareDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self):
        pass


    def delete(self):
        pass


    def _parse_share(self, data):
        share = TopicShare()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'topic_id' in data:
            try:
                share.topic_id = int(data['topic_id'])
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
