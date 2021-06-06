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
from app.modules.article.comment.favorite.favorite_dto import ArticleCommentFavoriteDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
ArticleComment = db.get_model('ArticleComment')
ArticleCommentFavorite = db.get_model('ArticleCommentFavorite')


class ArticleCommentFavoriteController(Controller):

    def create(self, article_comment_id):
        data = {}
        current_user = g.current_user
        comment = ArticleComment.query.get(article_comment_id)

        if not comment:
            return send_error(message=messages.ERR_NOT_FOUND)

        data['user_id'] = current_user.id
        data['article_comment_id'] = article_comment_id
        try:
            favorite = ArticleCommentFavorite.query.filter(ArticleCommentFavorite.user_id == data['user_id'],
                                             ArticleCommentFavorite.article_comment_id == data['article_comment_id']).first()
            if favorite:
                return send_result(message=messages.ERR_ALREADY_EXISTS)

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result( data=marshal(favorite, ArticleCommentFavoriteDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, article_comment_id, args):
        user_id, favorited_user_id, from_date, to_date = None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'favorited_user_id' in args:
            try:
                favorited_user_id = int(args['favorited_user_id'])
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
            query = ArticleCommentFavorite.query
            if article_comment_id is not None:
                query = query.filter(ArticleCommentFavorite.article_comment_id == article_comment_id)
            if user_id is not None:
                query = query.filter(ArticleCommentFavorite.user_id == user_id)
            if favorited_user_id is not None:
                query = query.filter(ArticleCommentFavorite.article_comment.user_id == favorited_user_id)
            if from_date is not None:
                query = query.filter(ArticleCommentFavorite.created_date >= from_date)
            if to_date is not None:
                query = query.filter(ArticleCommentFavorite.created_date <= to_date)
            favorites = query.all()
            if favorites is not None:
                return send_result(data=marshal(favorites, ArticleCommentFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            favorite = ArticleCommentFavorite.query.filter_by(id=object_id).first()
            if favorite is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            return send_result(data=marshal(favorite, ArticleCommentFavoriteDto.model_response), message='Success')

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))



    def update(self, object_id, data):
        pass


    def delete(self, article_comment_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            favorite = ArticleCommentFavorite.query.filter_by(article_comment_id=article_comment_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(favorite)
            db.session.commit()
            return send_result()
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = ArticleCommentFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'article_comment_id' in data:
            try:
                favorite.article_comment_id = int(data['article_comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return favorite
