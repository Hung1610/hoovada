#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from app.modules.topic.bookmark.bookmark_dto import TopicBookmarkDto
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Topic = db.get_model('Topic')
TopicBookmark = db.get_model('TopicBookmark')
User = db.get_model('User')

class TopicBookmarkController(Controller):
    query_classname = 'TopicBookmark'
    special_filtering_fields = ['from_date', 'to_date']
    allowed_ordering_fields = ['created_date', 'updated_date']

    def create(self, topic_id):
        if topic_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['topic_id'] = topic_id
        try:
            bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == data['user_id'], TopicBookmark.topic_id == data['topic_id']).first()
            if bookmark:
                return send_result(data=marshal(bookmark, TopicBookmarkDto.model_response))

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()

            return send_result( data=marshal(bookmark, TopicBookmarkDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(TopicBookmark.created_date >= params.get('from_date'))
        
        if params.get('to_date'):
            query = query.filter(TopicBookmark.created_date <= params.get('to_date'))

        return query

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            bookmarks = res.get('data')
            results = []
            for bookmark in bookmarks:
                result = bookmark._asdict()
                result['topic'] = bookmark.topic
                results.append(result)

            res['data'] = marshal(results, TopicBookmarkDto.model_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create_multiple_topics_bookmarks(self, args):
        
        if topic_ids in args:
            for topic_id in args['topic_ids']:
                try:
                    self.create(topic_id)
                except Exception as e:
                    print(e.__str__())
                    pass


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            bookmark = TopicBookmark.query.filter_by(id=object_id).first()
            if bookmark is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            return send_result(data=marshal(bookmark, TopicBookmarkDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self):
        pass


    def delete(self, topic_id):
        if topic_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        current_user = g.current_user
        user_id = current_user.id
        try:
            bookmark = TopicBookmark.query.filter_by(topic_id=topic_id, user_id=user_id).first()
            if bookmark is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(bookmark)
            db.session.commit()
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


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
