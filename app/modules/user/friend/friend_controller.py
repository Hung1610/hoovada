#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from common.utils.util import send_friend_request_notif_email
from common.utils.onesignal_notif import push_notif_to_specific_users
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, request, g
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from common.db import db
from app.constants import messages
from app.modules.user.friend.friend_dto import UserFriendDto
from common.controllers.controller import Controller
from common.models import Reputation, User, UserFriend
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFriendController(Controller):
    query_classname = 'UserFriend'
    special_filtering_fields = ['from_date', 'to_date', 'user_id']
    allowed_ordering_fields = ['created_date', 'updated_date']

    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(UserFriend.created_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(UserFriend.created_date <= dateutil.parser.isoparse(params.get('to_date')))
        if params.get('user_id'):
            g.friend_belong_to_user_id = params.get('user_id')
            query = query.filter(db.or_(UserFriend.friended_id == params.get('user_id'), UserFriend.friend_id == params.get('user_id')))

        return query

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            res['data'] = marshal(res['data'], UserFriendDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load error, please try again later.")

    def create(self, object_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['friend_id'] = current_user.id
        data['friended_id'] = object_id
        if data['friend_id'] == data['friended_id']:
            return send_result(message=messages.ERR_ISSUE.format('Cannot befriend self'))
        try:
            friend = UserFriend.query.filter(db.or_(\
                db.and_(UserFriend.friend_id == data['friend_id'], UserFriend.friended_id == data['friended_id']),\
                db.and_(UserFriend.friended_id == data['friend_id'], UserFriend.friend_id == data['friended_id']))).first()
            if friend:
                return send_result(message=messages.ERR_ISSUE.format('Already befriended'))

            friend = self._parse_friend(data=data, friend=None)
            db.session.add(friend)
            db.session.commit()
                        
            if friend.friended:
                if friend.friended.is_online\
                    and friend.friended.friend_request_notify_settings:
                    display_name =  current_user.display_name if current_user else 'Khách'
                    message = '[Thông báo] ' + display_name + ' đã yêu cầu làm bạn!'
                    push_notif_to_specific_users(message, [friend.friended.id])
                elif friend.friended.friend_request_email_settings:
                    send_friend_request_notif_email(friend.friended, current_user)
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Friend'),
                               data=marshal(friend, UserFriendDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Friend', e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
        friend = UserFriend.query.filter_by(id=object_id).first()
        if friend is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Friend', object_id))
        else:
            return send_result(data=marshal(friend, UserFriendDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def approve(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Friend', object_id))
                
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
                return send_error(message=messages.ERR_CREATE_FAILED.format('Friend', e))
            friend.is_approved = True
            db.session.commit()
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_ISSUE.format(e))

    def disapprove(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Friend', object_id))
                
            if friend.is_approved:
                return send_result(message='Already friend.')

            return self.delete(object_id)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_ISSUE.format(e))
        
    def delete(self, object_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            UserFriend.query.filter(\
                    ((UserFriend.friend_id == object_id) & (UserFriend.friended_id == user_id)) |\
                    ((UserFriend.friended_id == object_id) & (UserFriend.friend_id == user_id)) \
                ).delete(synchronize_session=False)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS.format('Friend'))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Friend', e))

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
