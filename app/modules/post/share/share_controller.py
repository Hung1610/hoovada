#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask_restx import marshal
from flask import request, current_app
from sqlalchemy import desc

# own modules
from app import db
from app.constants import messages
from common.controllers.controller import Controller
from app.modules.post.post import Post
from app.modules.post.share.share import PostShare
from app.modules.post.share.share_dto import ShareDto
from app.modules.user.user import User
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType
from common.utils.permission import has_permission

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class ShareController(Controller):
    def get(self, post_id, args):
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

        query = PostShare.query
        if user_id is not None:
            query = query.filter(PostShare.user_id == user_id)
        if post_id is not None:
            query = query.filter(PostShare.post_id == post_id)
        if from_date is not None:
            query = query.filter(PostShare.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PostShare.created_date <= to_date)
        if facebook is not None:
            query = query.filter(PostShare.facebook == facebook)
        if twitter is not None:
            query = query.filter(PostShare.twitter == twitter)
        if zalo is not None:
            query = query.filter(PostShare.zalo == zalo)
        shares = query.all()
        if len(shares) > 0:
            return send_result(data=marshal(shares, ShareDto.model_response), message='Success')
        else:
            return send_result(messages.ERR_NOT_FOUND.format('Post Share'))

    def create(self, post_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        current_user, _ = current_app.get_logged_user(request)
        if not has_permission(current_user.id, PermissionType.SHARE):
            return send_error(code=401, message='You have no authority to perform this action')

        data['user_id'] = current_user.id
        data['post_id'] = post_id
        try:
            share = self._parse_share(data=data)
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                post = Post.query.filter_by(id=share.post_id).first()
                if not post:
                    return send_error(message=messages.ERR_NOT_FOUND.format('Post'))
                user_voted = User.query.filter_by(id=post.user_id).first()
                if not user_voted:
                    return send_error(message=messages.ERR_NOT_FOUND.format('User'))
                user_voted.post_shared_count += 1
                if current_user:
                    share.user_id = current_user.id
                    current_user.post_share_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result(data=marshal(share, ShareDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Post Share', e))

    def get_by_id(self, object_id):
        query = PostShare.query
        share = query.filter(PostShare.id == object_id).first()
        if share is None:
            return send_error(message=messages.ERR_NOT_FOUND.format('Post Share'))
        else:
            return send_result(data=marshal(share, ShareDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data):
        share = PostShare()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'post_id' in data:
            try:
                share.post_id = int(data['post_id'])
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
