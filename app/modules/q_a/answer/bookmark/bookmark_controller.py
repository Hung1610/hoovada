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
from app.modules.q_a.answer.bookmark import constants
from app.modules.q_a.answer.bookmark.bookmark_dto import AnswerBookmarkDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


AnswerBookmark = db.get_model('AnswerBookmark')
Answer = db.get_model('Answer')
User = db.get_model('User')


class AnswerBookmarkController(Controller):
    def get(self, answer_id, args):
        
        try:
            user_id = args.get('user_id', None)
            bookmarkd_user_id = args.get('bookmarkd_user_id', None)
            from_date = args.get('from_date', None)
            to_date = args.get('to_date', None)

            query = AnswerBookmark.query
            if answer_id is not None:
                query = query.filter(AnswerBookmark.answer_id == answer_id)
            if user_id is not None:
                query = query.filter(AnswerBookmark.user_id == user_id)
            if bookmarkd_user_id is not None:
                query = query.filter(AnswerBookmark.answer.user_id == bookmarkd_user_id)
            if from_date is not None:
                query = query.filter(AnswerBookmark.created_date >= from_date)
            if to_date is not None:
                query = query.filter(AnswerBookmark.created_date <= to_date)
            bookmarks = query.all()
            if bookmarks is not None and len(bookmarks) > 0:
                return send_result(data=marshal(bookmarks, AnswerBookmarkDto.model_response), message='Success')
            else:
                return send_result(message=constants.msg_answer_bookmark_not_found)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format("all answer bookmark", str(e)))


    def create(self, answer_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == data['user_id'],
                                             AnswerBookmark.answer_id == data['answer_id']).first()
            if bookmark:
                return send_result(message=constants.msg_already_bookmarkd)

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()
            return send_result(message=constants.msg_create_success,
                               data=marshal(bookmark, AnswerBookmarkDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_create_failed)

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        bookmark = AnswerBookmark.query.filter_by(id=object_id).first()
        if bookmark is None:
            return send_error(message=constants.msg_answer_bookmark_not_found)
        else:
            return send_result(data=marshal(bookmark, AnswerBookmarkDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, answer_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            bookmark = AnswerBookmark.query.filter_by(answer_id=answer_id, user_id=user_id).first()
            if bookmark is None:
                return send_error(message=constants.msg_answer_bookmark_not_found)
            else:
                db.session.delete(bookmark)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(bookmark.id))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_delete_failed)

    def _parse_bookmark(self, data, bookmark=None):
        if bookmark is None:
            bookmark = AnswerBookmark()
        if 'user_id' in data:
            try:
                bookmark.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
            try:
                bookmark.answer_id = int(data['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return bookmark
