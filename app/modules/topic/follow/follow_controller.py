#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, g, request
from flask_restx import marshal

# own modules
from app.app import db
from app.constants import messages
from app.modules.topic.follow.follow_dto import TopicFollowDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

User = db.get_model('User')
Topic = db.get_model('Topic')
TopicFollow = db.get_model('TopicFollow')

class TopicFollowController(Controller):
    def get(self, args, topic_id=None):
        '''
        Get/Search follows.

        Args:
             The dictionary-like parameters.

        Returns:
        '''
        
        user_id, followed_user_id, from_date, to_date = None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'followed_user_id' in args:
            try:
                followed_user_id = int(args['followed_user_id'])
            except Exception as e:
                print(e.__str__())
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

        query = TopicFollow.query
        if topic_id is not None:
            query = query.filter(TopicFollow.topic_id == topic_id)
        if user_id is not None:
            query = query.filter(TopicFollow.user_id == user_id)
        if followed_user_id is not None:
            query = query.filter(TopicFollow.topic.user_id == followed_user_id)
        if from_date is not None:
            query = query.filter(TopicFollow.created_date >= from_date)
        if to_date is not None:
            query = query.filter(TopicFollow.created_date <= to_date)

        follows = query.all()

        return send_result(data=marshal(follows, TopicFollowDto.model_response), message='Success')

    def create(self, topic_id):
        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['topic_id'] = topic_id
        topic = Topic.query.get(topic_id)
        if not topic:
            return send_error(message=messages.ERR_NOT_FOUND.format('Topic'))
        if not topic.allow_follow:
            return send_error(message=messages.ERR_ISSUE.format('Comment does not allow voting.'))
        try:
            follow = TopicFollow.query.filter(TopicFollow.user_id == data['user_id'],
                                             TopicFollow.topic_id == data['topic_id']).first()
            if follow:
                return send_result(message=messages.ERR_ISSUE.format('Topic already followed'))

            follow = self._parse_follow(data=data, follow=None)
            follow.created_date = datetime.utcnow()
            follow.updated_date = datetime.utcnow()
            db.session.add(follow)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Topic'),
                               data=marshal(follow, TopicFollowDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Topic Follow', e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Id"))
        follow = TopicFollow.query.filter_by(id=object_id).first()
        if follow is None:
            return send_error(message=messages.ERR_NOT_FOUND.format('Topic Follow'))
        else:
            return send_result(data=marshal(follow, TopicFollowDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        try:
            follow = TopicFollow.query.filter_by(id=object_id).first()
            if follow is None:
                return send_error(message=messages.ERR_NOT_FOUND.format('Topic Follow'))
            else:
                db.session.delete(follow)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format('Topic Follow'))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Topic Follow', e))

    def delete_for_current_user(self, topic_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            follow = TopicFollow.query.filter_by(topic_id=topic_id, user_id=user_id).first()
            if follow is None:
                return send_error(message=messages.ERR_NOT_FOUND.format('Topic Follow'))
            else:
                db.session.delete(follow)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format('Topic Follow'))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Topic Follow', e))

    def _parse_follow(self, data, follow=None):
        if follow is None:
            follow = TopicFollow()
        if 'user_id' in data:
            try:
                follow.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in data:
            try:
                follow.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return follow
