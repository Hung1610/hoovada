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
from app.modules.article.favorite import constants
from app.modules.article.favorite.favorite_dto import FavoriteDto
from common.controllers.controller import Controller
from common.models import Article, ArticleComment, ArticleFavorite, User
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class FavoriteController(Controller):
    def get(self, article_id, args):
        
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

        query = ArticleFavorite.query
        if article_id is not None:
            query = query.filter(ArticleFavorite.article_id == article_id)
        if user_id is not None:
            query = query.filter(ArticleFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(ArticleFavorite.article.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(ArticleFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(ArticleFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, FavoriteDto.model_response), message='Success')
        else:
            return send_result(message=constants.msg_article_favorite_not_found)

    def create(self, article_id):
        data = {}
        current_user = g.current_user
        if not has_permission(current_user.id, PermissionType.FAVORITE):
            return send_error(code=401, message='You have no authority to perform this action')

        data['user_id'] = current_user.id
        data['article_id'] = article_id
        data = self.add_org_data(data)
        try:
            favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == data['user_id'],
                                             ArticleFavorite.article_id == data['article_id'],
                                             ArticleFavorite.entity_type == data['role']).first()
            if favorite:
                return send_result(message=constants.msg_already_favorited)

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message=constants.msg_create_success,
                               data=marshal(favorite, FavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_create_failed)

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        favorite = ArticleFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message=constants.msg_article_favorite_not_found)
        else:
            return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, article_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            favorite = ArticleFavorite.query.filter_by(article_id=article_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message=constants.msg_article_favorite_not_found)
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(favorite.id))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_delete_failed)

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = ArticleFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'article_id' in data:
            try:
                favorite.article_id = int(data['article_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'entity_type' in data:
            try:
                favorite.entity_type = data['entity_type']
            except Exception as e:
                print(e.__str__())
                pass

        if 'organization_id' in data:
            try:
                favorite.organization_id = int(data['organization_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return favorite
