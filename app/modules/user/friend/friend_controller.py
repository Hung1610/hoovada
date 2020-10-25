#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request, current_app
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from app import db
from common.controllers.controller import Controller
from app.modules.user.user import User
from app.modules.user.friend.friend import UserFriend
from app.modules.user.friend.friend_dto import UserFriendDto
from app.modules.user.user import User
from app.modules.user.reputation.reputation import Reputation
from common.utils.response import send_error, send_result
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFriendController(Controller):
    def get(self, object_id, args):
        '''
        Get/Search friends.

        Args:
             The dictionary-like parameters.

        Returns:
        '''
        
        friend_id, from_date, to_date = None, None, None
        if 'friend_id' in args:
            try:
                friend_id = int(args['friend_id'])
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

        query = UserFriend.query
        if object_id is not None:
            query = query.filter(UserFriend.friended_id == object_id)
        if friend_id is not None:
            query = query.filter(UserFriend.friend_id == friend_id)
        if from_date is not None:
            query = query.filter(UserFriend.created_date >= from_date)
        if to_date is not None:
            query = query.filter(UserFriend.created_date <= to_date)
        friends = query.all()
        if friends is not None and len(friends) > 0:
            return send_result(data=marshal(friends, UserFriendDto.model_response), message='Success')
        else:
            return send_result(message=messages.MSG_NOT_FOUND.format('Friend'))

    def create(self, object_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['friend_id'] = current_user.id
        data['friended_id'] = object_id
        try:
            friend = UserFriend.query.filter(UserFriend.friend_id == data['friend_id'],
                                             UserFriend.friended_id == data['friended_id']).first()
            if friend:
                return send_result(message=messages.MSG_ISSUE.format('Already befriended'))

            friend = self._parse_friend(data=data, friend=None)
            db.session.add(friend)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Friend'),
                               data=marshal(friend, UserFriendDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Friend', e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('object_id'))
        friend = UserFriend.query.filter_by(id=object_id).first()
        if friend is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Friend', object_id))
        else:
            return send_result(data=marshal(friend, UserFriendDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def approve(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('object_id'))
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Friend', object_id))
                
            # if friend.is_approved:
            #     return send_result(message='Already friend.')

            actual_friend = UserFriend.query.filter(UserFriend.friend_id == friend.friended_id,
                                                UserFriend.friended_id == friend.friend_id).first()
            if actual_friend:
                return send_result(message='Already friend.')
            data = {}
            data['friend_id'] = friend.friended_id
            data['friended_id'] = friend.friend_id
            try:
                actual_friend = self._parse_friend(data=data, friend=None)
                db.session.merge(actual_friend)
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.MSG_CREATE_FAILED.format('Friend', e))
            friend.is_approved = True
            db.session.commit()
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_ISSUE.format(e))

    def disapprove(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('object_id'))
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Friend', object_id))
                
            if friend.is_approved:
                return send_result(message='Already friend.')

            return self.delete(object_id)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_ISSUE.format(e))
        
    def delete(self, object_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            friend = UserFriend.query.filter_by(friend_id=object_id, friended_id=user_id).first()
            if friend is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Friend', object_id))
            else:
                db.session.delete(friend)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format('Friend'))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_DELETE_FAILED.format('Friend', e))

    def get_top_users(self, args, object_id):
        try:
            limit, topics = None, None
            if args.get('limit'):
                limit = int(args['limit'])
            else:
                return send_error(message='Please provide limit')
            if args.get('topic'):
                topics = args['topic']

            friend_ids = UserFriend.query.filter(UserFriend.friended_id == object_id).with_entities(UserFriend.friend_id).all()
            query = db.session.query(
                    User,
                    db.func.sum(Reputation.score).label('total_score'),
                )\
                .filter(User.id.in_(friend_ids))
            if topics:
                query = query.filter(Reputation.topic_id.in_(topics))
            top_users = query\
                .group_by(User,)\
                .order_by(db.desc('total_score'))\
                .limit(limit)\
                .all()
            results = [{'user': user, 'total_score': total_score} for user, total_score in top_users]
            return send_result(data=marshal(results, UserFriendDto.top_user_friend_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get recommended users failed. Error: " + e.__str__())

    def _parse_friend(self, data, friend=None):
        if friend is None:
            friend = UserFriend()
        if 'friend_id' in data:
            try:
                friend.friend_id = int(data['friend_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'friended_id' in data:
            try:
                friend.friended_id = int(data['friended_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return friend
