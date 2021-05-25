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
from common.cache import cache
from app.modules.q_a.question.bookmark.bookmark_dto import QuestionBookmarkDto
from common.controllers.controller import Controller
from common.models import Question, User
from common.models.bookmark import QuestionBookmark
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionBookmarkController(Controller):

    def create(self, question_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['question_id'] = question_id
        try:
            bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == data['user_id'],
                                             QuestionBookmark.question_id == data['question_id']).first()
            if bookmark:
                return send_error(message=messages.ERR_ALREADY_EXISTS)

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(bookmark, QuestionBookmarkDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):
        
        try:
            user_id = args.get('user_id', None)
            bookmarkd_user_id = args.get('bookmarkd_user_id', None)
            from_date = args.get('from_date', None)
            to_date = args.get('to_date', None)
            question_id = args.get('question_id', None)

            query = QuestionBookmark.query
            if question_id is not None:
                query = query.filter(QuestionBookmark.question_id == question_id)
            if user_id is not None:
                query = query.filter(QuestionBookmark.user_id == int(user_id))
            if bookmarkd_user_id is not None:
                query = query.filter(QuestionBookmark.question.user_id == int(bookmarkd_user_id))
            if from_date is not None:
                query = query.filter(QuestionBookmark.created_date >= dateutil.parser.isoparse(from_date))
            if to_date is not None:
                query = query.filter(QuestionBookmark.created_date <= dateutil.parser.isoparse(to_date))

            bookmarks = query.all()
            if bookmarks is not None:
                return send_result(data=marshal(bookmarks, QuestionBookmarkDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            bookmark = QuestionBookmark.query.filter_by(id=object_id).first()
            if bookmark is None:
                return send_error(message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        pass


    def delete(self, question_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            bookmark = QuestionBookmark.query.filter_by(question_id=question_id, user_id=user_id).first()
            if bookmark is None:
                return send_result(message=messages.ERR_NOT_FOUND)
           
            db.session.delete(bookmark)
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)
            eturn send_result(message=messages.MSG_DELETE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_bookmark(self, data, bookmark=None):
        if bookmark is None:
            bookmark = QuestionBookmark()

        if 'user_id' in data:
            try:
                bookmark.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'question_id' in data:
            try:
                bookmark.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return bookmark
