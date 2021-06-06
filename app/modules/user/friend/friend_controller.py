#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from common.models.follow import UserFollow
from app.modules.search.search_controller import ESUserFriend
from common.utils.util import send_friend_request_notif_email
from common.db import db
from app.constants import messages
from app.modules.user.friend.friend_dto import UserFriendDto
from common.dramatiq_producers import push_notif_to_specific_users_produce
from common.controllers.controller import Controller
from common.models import Reputation, User, UserFriend
from common.utils.response import paginated_result, send_error, send_result
from app.modules.user.follow.follow_controller import UserFollowController
from common.es import get_model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

ESUserFriend = get_model('UserFriend')


class UserFriendController(Controller):
    query_classname = 'UserFriend'
    special_filtering_fields = ['from_date', 'to_date', 'user_id', 'display_name', 'is_mutual']
    allowed_ordering_fields = ['created_date', 'updated_date']


    def get_query(self):
        query = self.get_model_class().query
        query = query.filter((UserFriend.friend.has(User.is_deactivated == False)) &\
            (UserFriend.friended.has(User.is_deactivated == False))
        )
        return query


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(UserFriend.created_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(UserFriend.created_date <= dateutil.parser.isoparse(params.get('to_date')))
        if params.get('user_id'):
            g.friend_belong_to_user_id = params.get('user_id')
            query = query.filter(db.or_(UserFriend.friended_id == params.get('user_id'), UserFriend.friend_id == params.get('user_id')))
        if params.get('display_name'):
            query = query.filter(
                (UserFriend.friend.has(User.display_name.like('%' + params.get('display_name') + '%'))) |
                (UserFriend.friended.has(User.display_name.like('%' + params.get('display_name') + '%'))))

        return query


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            res['data'] = marshal(res['data'], UserFriendDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, object_id):
        data = {}
        current_user = g.current_user
        data['friend_id'] = current_user.id
        data['friended_id'] = object_id

        if data['friend_id'] == data['friended_id']:
            return send_result(message=messages.ERR_ISSUE.format('Cannot befriend self'))

        try:
            friend_entity = UserFriend.query.filter(db.or_(\
                db.and_(UserFriend.friend_id == data['friend_id'], UserFriend.friended_id == data['friended_id']),\
                db.and_(UserFriend.friended_id == data['friend_id'], UserFriend.friend_id == data['friended_id']))).first()
            if friend_entity:
                return send_result(message=messages.ERR_ISSUE.format('Already befriended'))

            friend = self._parse_friend(data=data, friend=None)
            db.session.add(friend)
            db.session.flush()
            user_friend_dsl = ESUserFriend(_id=friend.id, friend_id=friend.friend_id, friended_id=friend.friended_id,
                                     friend_display_name=friend.friend.display_name, friend_email=friend.friend.email, friend_profile_pic_url=friend.friend.profile_pic_url,
                                     friended_display_name=friend.friended.display_name, friended_email=friend.friended.email, friended_profile_pic_url=friend.friended.profile_pic_url, is_approved=friend.is_approved)
            user_friend_dsl.save()
            db.session.commit()
                        
            # also following the person
            try:
                user_follow_controller = UserFollowController()
                user_follow_controller.create(object_id)
            except Exception as e:
                print(e.__str__())
                pass


            if friend.friended:
                if friend.friended.is_online and friend.friended.friend_request_notify_settings:
                    display_name =  current_user.display_name if current_user else 'Khách'
                    message = display_name + ' đã yêu cầu làm bạn!'
                    push_notif_to_specific_users_produce(message, [friend.friended.id])
                elif friend.friended.friend_request_email_settings:
                    send_friend_request_notif_email(friend.friended, current_user)

            return send_result( data=marshal(friend, UserFriendDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))

        try:
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            return send_result(data=marshal(friend, UserFriendDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self):
        pass


    def approve(self, object_id):
        current_user = g.current_user
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))        
        
        try:

            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Friend', object_id))

            if friend.is_approved is True:
                return send_result(message='Already friend.')
            user_friend_dsl = ESUserFriend(_id=friend.id)
            user_friend_dsl.update(is_approved=1)
            # also following back the person
            try:
                user_follow_controller = UserFollowController()
                if friend.friended_id == current_user.id:
                    user_follow_controller.create(friend.friend_id)
                elif friend.friend_id == current_user.id:
                    user_follow_controller.create(friend.friended_id)

            except Exception as e:
                print(e.__str__())
                pass

            friend.is_approved = True
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def disapprove(self, object_id):
        current_user = g.current_user
        user_id = current_user.id
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))

        try:
            friend = UserFriend.query.filter_by(id=object_id).first()
            if friend is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Friend', object_id))
                
            if friend.is_approved:
                return send_result(message='Already friend.')

            if friend.friend_id == user_id:
                friended_id = friend.friended_id
            if friend.friended_id == user_id:
                friended_id = friend.friend_id
            return self.delete(friended_id)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

      
    def delete(self, object_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            user_friends = UserFriend.query.filter(\
                    ((UserFriend.friend_id == object_id) & (UserFriend.friended_id == user_id)) |\
                    ((UserFriend.friended_id == object_id) & (UserFriend.friend_id == user_id)) \
                ).all()
            try:
                for user_friend in user_friends:
                    print('--wewew---', user_friend.id)
                    db.session.delete(user_friend)
                    user_friend_dsl = ESUserFriend(_id=user_friend.id)
                    user_friend_dsl.delete()
            except Exception as e:
                print(e.__str__())
                pass
            db.session.commit()

            # TODO: need to remove following if remove friend
            follow = UserFollow.query.filter_by(followed_id=object_id, follower_id=user_id).first()
            if follow:
                db.session.delete(follow)
                db.session.commit()

            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


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
            return send_result(data=marshal(results, UserFriendDto.top_user_friend_response))
        except Exception as e:
            print(e)
            return send_error(message=messages.ERR_GET_FAILED.format(e))


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
