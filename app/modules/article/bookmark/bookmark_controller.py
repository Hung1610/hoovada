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
from app.modules.article.bookmark.bookmark_dto import ArticleBookmarkDto
from common.utils.response import paginated_result
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result
from common.models.bookmark import ArticleBookmark
from common.models import Article, User

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2021 hoovada.com . All Rights Reserved."


class ArticleBookmarkController(Controller):
    def create(self, article_id):
        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['article_id'] = article_id
        data = self.add_org_data(data)
        try:
            bookmark = ArticleBookmark.query.filter(
                ArticleBookmark.user_id == data['user_id'], 
                ArticleBookmark.article_id == data['article_id'],
                ArticleBookmark.entity_type == data['entity_type']).first()
            if bookmark:
                return send_result( data=marshal(bookmark, ArticleBookmarkDto.model_response))

            bookmark = self._parse_bookmark(data=data, bookmark=None)
            bookmark.created_date = datetime.utcnow()
            bookmark.updated_date = datetime.utcnow()
            db.session.add(bookmark)
            db.session.commit()

            return send_result( data=marshal(bookmark, ArticleBookmarkDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(ArticleBookmark.created_date >= params.get('from_date'))
        if params.get('to_date'):
            query = query.filter(ArticleBookmark.created_date <= params.get('to_date'))

        return query


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            bookmarks = res.get('data')
            results = []
            for bookmark in bookmarks:
                result = bookmark._asdict()
                result['article'] = bookmark.article
                results.append(result)

            res['data'] = marshal(results, ArticleBookmarkDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
        
        bookmark = ArticleBookmark.query.filter_by(id=object_id).first()
        if bookmark is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        
        return send_result(data=marshal(bookmark, ArticleBookmarkDto.model_response))



    def update(self, object_id, data):
        pass


    def delete(self, article_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            bookmark = ArticleBookmark.query.filter_by(article_id=article_id, user_id=user_id).first()
            if bookmark is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                db.session.delete(bookmark)
                db.session.commit()
                return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_bookmark(self, data, bookmark=None):
        if bookmark is None:
            bookmark = ArticleBookmark()
            
        if 'user_id' in data:
            try:
                bookmark.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'article_id' in data:
            try:
                bookmark.article_id = int(data['article_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'entity_type' in data:
            try:
                bookmark.entity_type = data['entity_type']
            except Exception as e:
                print(e.__str__())
                pass

        if 'organization_id' in data:
            try:
                bookmark.organization_id = int(data['organization_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return bookmark
