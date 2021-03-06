#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.user.follow.follow_dto import UserFollowDto
from common.controllers.controller import Controller
from common.models import Reputation, User, UserFollow
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFollowController(Controller):

    def get(self, object_id, args):
        
        follower_id, from_date, to_date = None, None, None
        if 'follower_id' in args:
            try:
                follower_id = int(args['follower_id'])
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

        try:
            query = UserFollow.query
            if object_id is not None:
                query = query.filter(UserFollow.followed_id == object_id)
            
            if follower_id is not None:
                query = query.filter(UserFollow.follower_id == follower_id)
            
            if from_date is not None:
                query = query.filter(UserFollow.created_date >= from_date)

            if to_date is not None:
                query = query.filter(UserFollow.created_date <= to_date)
            follows = query.all()

            return send_result(data=marshal(follows, UserFollowDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, object_id):
        
        current_user = g.current_user
        data = {}
        data['follower_id'] = current_user.id
        data['followed_id'] = object_id

        if data['follower_id'] == data['followed_id']:
            return send_result(message=messages.ERR_SEND_REQUEST_TO_ONESELF)

        try:
            follow = UserFollow.query.filter(UserFollow.follower_id == data['follower_id'],
                                             UserFollow.followed_id == data['followed_id']).first()
            if follow is not None:
                return send_result(message=messages.ERR_ALREADY_EXISTS)

            follow = self._parse_follow(data=data, follow=None)
            db.session.add(follow)
            db.session.commit()

            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))

        try:
            follow = UserFollow.query.filter_by(id=object_id).first()
            if follow is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                return send_result(data=marshal(follow, UserFollowDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        pass


    def delete(self, object_id):
        current_user = g.current_user
        user_id = current_user.id

        try:
            follow = UserFollow.query.filter_by(followed_id=object_id, follower_id=user_id).first()
            if follow is None:
                return send_result(message=messages.ERR_NOT_FOUND)

            db.session.delete(follow)
            db.session.commit()
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_top_users(self, object_id, args):
        try:
            limit, topics = None, None
            if args.get('limit'):
                limit = int(args['limit'])
            else:
                return send_error(message='Please provide limit')
            if args.get('topic'):
                topics = args['topic']

            follower_ids = UserFollow.query.filter(UserFollow.followed_id == object_id).with_entities(UserFollow.follower_id).all()
            query = db.session.query(
                    User,
                    db.func.sum(Reputation.score).label('total_score'),
                )\
                .filter(User.id.in_(follower_ids))
            if topics:
                query = query.filter(Reputation.topic_id.in_(topics))
            top_users = query\
                .group_by(User,)\
                .order_by(db.desc('total_score'))\
                .limit(limit)\
                .all()
            results = [{'user': user, 'total_score': total_score} for user, total_score in top_users]
            return send_result(data=marshal(results, UserFollowDto.top_user_followee_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_follow(self, data, follow=None):
        if follow is None:
            follow = UserFollow()

        if 'follower_id' in data:
            try:
                follow.follower_id = int(data['follower_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'followed_id' in data:
            try:
                follow.followed_id = int(data['followed_id'])
            except Exception as e:
                print(e.__str__())
                pass

        return follow