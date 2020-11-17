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
from app.app import db
from app.modules.topic.bookmark import constants
from app.modules.topic.bookmark.bookmark_dto import TopicBookmarkDto
from common.controllers.controller import Controller
from common.models import Topic, TopicBookmark, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicBookmarkController(Controller):
    def get(self, args, topic_id=None):
        '''
        Get/Search bookmarks.

        Args:
             The dictionary-like parameters.

        Returns:
        '''
        
        user_id, bookmarkd_user_id, from_date, to_date = None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'bookmarkd_user_id' in args:
            try:
                bookmarkd_user_id = int(args['bookmarkd_user_id'])
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

        query = TopicBookmark.query
        if topic_id is not None:
            query = query.filter(TopicBookmark.topic_id == topic_id)
        if user_id is not None:
            query = query.filter(TopicBookmark.user_id == user_id)
        if bookmarkd_user_id is not None:
            query = query.filter(TopicBookmark.topic.user_id == bookmarkd_user_id)
        if from_date is not None:
            query = query.filter(TopicBookmark.created_date >= from_date)
        if to_date is not None:
            query = query.filter(TopicBookmark.created_date <= to_date)
        results = []
        for bookmark in query:
            result = bookmark._asdict()
            result['topic'] = bookmark.topic
            results.append(result)
        return send_result(data=marshal(results, TopicBookmarkDto.model_response), message='Success')

    def create(self, topic_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        data['topic_id'] = topic_id
        try:
            bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == data['user_id'],
                                             TopicBookmark.topic_id == data['topic_id']).first()
            if bookmark:
                return send_result(message=constants.msg_already_bookmarkd)

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()
            return send_result(message=constants.msg_create_success,
                               data=marshal(bookmark, TopicBookmarkDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_create_failed)

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        bookmark = TopicBookmark.query.filter_by(id=object_id).first()
        if bookmark is None:
            return send_error(message=constants.msg_topic_bookmark_not_found)
        else:
            return send_result(data=marshal(bookmark, TopicBookmarkDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, topic_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            bookmark = TopicBookmark.query.filter_by(topic_id=topic_id, user_id=user_id).first()
            if bookmark is None:
                return send_error(message=constants.msg_topic_bookmark_not_found)
            else:
                db.session.delete(bookmark)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(bookmark.id))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_delete_failed)

    def _parse_bookmark(self, data, bookmark=None):
        if bookmark is None:
            bookmark = TopicBookmark()
        if 'user_id' in data:
            try:
                bookmark.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in data:
            try:
                bookmark.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return bookmark
