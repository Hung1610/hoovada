#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.article.article import Article
from app.modules.article.comment.comment import Comment
from app.modules.article.favorite import constants
from app.modules.article.favorite.favorite import Favorite
from app.modules.article.favorite.favorite_dto import FavoriteDto
from app.modules.user.user import User
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class FavoriteController(Controller):
<<<<<<< HEAD
    def search(self, args):
        """
        Search favorites.
=======
    def get(self, article_id, args):
        '''
        Get/Search favorites.
>>>>>>> dev

        :param args: The dictionary-like parameters.

        :return:
        """
        if not isinstance(args, dict):
            return send_error(message=constants.msg_wrong_data_format)
        user_id, favorited_user_id, from_date, to_date = None, None, None, None, None, None, None
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
        if user_id is None and favorited_user_id is None and from_date is None and to_date is None:
            return send_error(message=constants.msg_lacking_query_params)

        query = Favorite.query
        if user_id is not None:
            query = query.filter(Favorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(Favorite.article.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(Favorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(Favorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, FavoriteDto.model_response), message='Success')
        else:
            return send_result(message=constants.msg_article_favorite_not_found)

    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)
        current_user, _ = AuthController.get_logged_user(request)
        data['user_id'] = current_user.id
        data['article_id'] = article_id
        try:
            favorite = Favorite.query.filter(Favorite.user_id == data['user_id'],
                                             Favorite.article_id == data['article_id']).first()
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
        favorite = Favorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message=constants.msg_article_favorite_not_found)
        else:
            return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, article_id):
        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = Favorite.query.filter_by(article_id=article_id, user_id=user_id).first()
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
            favorite = Favorite()
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
        # if 'favorite_date' in data:
        #     try:
        #         favorite.favorite_date = dateutil.parser.isoparse(data['favorite_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        return favorite
