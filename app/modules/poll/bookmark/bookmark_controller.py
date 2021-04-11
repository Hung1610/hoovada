#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from common.db import db
from app.constants import messages
from app.modules.poll.bookmark.bookmark_dto import PollBookmarkDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


PollBookmark = db.get_model('PollBookmark')
Poll = db.get_model('Poll')
User = db.get_model('User')


class PollBookmarkController(Controller):
    def get(self, poll_id, args):
        
        try:
            user_id = args.get('user_id', None)
            bookmarkd_user_id = args.get('bookmarkd_user_id', None)
            from_date = args.get('from_date', None)
            to_date = args.get('to_date', None)

            query = PollBookmark.query
            if poll_id is not None:
                query = query.filter(PollBookmark.poll_id == poll_id)
            if user_id is not None:
                query = query.filter(PollBookmark.user_id == user_id)
            if bookmarkd_user_id is not None:
                query = query.filter(PollBookmark.poll.user_id == bookmarkd_user_id)
            if from_date is not None:
                query = query.filter(PollBookmark.created_date >= from_date)
            if to_date is not None:
                query = query.filter(PollBookmark.created_date <= to_date)
            bookmarks = query.all()
            if bookmarks is not None and len(bookmarks) > 0:
                return send_result(data=marshal(bookmarks, PollBookmarkDto.model_response), message='Success')
            else:
                return send_result(message=messages.ERR_NOT_FOUND)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format("all poll bookmark", str(e)))


    def create(self, poll_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        data['poll_id'] = poll_id
        try:
            bookmark = PollBookmark.query.filter(PollBookmark.user_id == data['user_id'],
                                             PollBookmark.poll_id == data['poll_id']).first()
            if bookmark:
                return send_error(message=messages.ERR_CREATE_FAILED.format('Poll User Select', 'This poll user select has already existed!'), data={'user_id': data['user_id'], 'poll_id': data['poll_id']})

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('PollBookmark'),
                               data=marshal(bookmark, PollBookmarkDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('PollBookmark', str(e)))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('poll bookmark id'))
        bookmark = PollBookmark.query.filter_by(id=object_id).first()
        if bookmark is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        else:
            return send_result(data=marshal(bookmark, PollBookmarkDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, poll_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            bookmark = PollBookmark.query.filter_by(poll_id=poll_id, user_id=user_id).first()
            if bookmark is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                db.session.delete(bookmark)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format(bookmark.id))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('PollBookmark', e))

    def _parse_bookmark(self, data, bookmark=None):
        if bookmark is None:
            bookmark = PollBookmark()
        if 'user_id' in data:
            try:
                bookmark.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'poll_id' in data:
            try:
                bookmark.poll_id = int(data['poll_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return bookmark
