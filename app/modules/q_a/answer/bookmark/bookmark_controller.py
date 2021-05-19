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

    def create(self, answer_id):

        if answer_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == data['user_id'],
                                             AnswerBookmark.answer_id == data['answer_id']).first()
            if bookmark:
                return send_result(message=messages.ERR_ALREADY_EXISTS)

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS,
                               data=marshal(bookmark, AnswerBookmarkDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, answer_id, args):
        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        user_id = args.get('user_id', None)
        bookmarkd_user_id = args.get('bookmarkd_user_id', None)
        from_date = args.get('from_date', None)
        to_date = args.get('to_date', None)

        try:
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
                return send_result(data=marshal(bookmarks, AnswerBookmarkDto.model_response), message=messages.MSG_GET_SUCCESS)
            else:
                return send_result(message=messages.ERR_NOT_FOUND)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            bookmark = AnswerBookmark.query.filter_by(id=object_id).first()
            if bookmark is None:
                return send_result(message=messages.ERR_NOT_FOUND)

            return send_result(data=marshal(bookmark, AnswerBookmarkDto.model_response), message=messages.MSG_GET_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        pass


    def delete(self, answer_id):
        if answer_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))      

        current_user = g.current_user
        user_id = current_user.id
        try:
            bookmark = AnswerBookmark.query.filter_by(answer_id=answer_id, user_id=user_id).first()
            if bookmark is None:
                return send_result(message=messages.ERR_NOT_FOUND)
            db.session.delete(bookmark)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


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
