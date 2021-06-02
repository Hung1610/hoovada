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
from app.modules.post.favorite.favorite_dto import FavoriteDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

User = db.get_model('User')
Post = db.get_model('Post')
PostComment = db.get_model('PostComment')
PostFavorite = db.get_model('PostFavorite')


class FavoriteController(Controller):

    def create(self, post_id):
        data = {}
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['post_id'] = post_id
        post = Post.query.get(post_id)
        
        if not post:
            return send_error(message=messages.ERR_NOT_FOUND)

        if not post.allow_favorite:
            return send_error(message=messages.ERR_FAVORITE_NOT_ALLOWED)
        
        try:
            favorite = PostFavorite.query.filter(PostFavorite.user_id == data['user_id'], PostFavorite.post_id == data['post_id']).first()
            if favorite:
                return send_result(message=messages.ERR_ALREADY_EXISTS)

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(favorite, FavoriteDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, post_id, args):
        
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
            query = PostFavorite.query
            if post_id is not None:
                query = query.filter(PostFavorite.post_id == post_id)
            if user_id is not None:
                query = query.filter(PostFavorite.user_id == user_id)
            if favorited_user_id is not None:
                query = query.filter(PostFavorite.post.user_id == favorited_user_id)
            if from_date is not None:
                query = query.filter(PostFavorite.created_date >= from_date)
            if to_date is not None:
                query = query.filter(PostFavorite.created_date <= to_date)
            favorites = query.all()
            return send_result(data=marshal(favorites, FavoriteDto.model_response), message=messages.MSG_GET_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            favorite = PostFavorite.query.filter_by(id=object_id).first()

            if favorite is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            return send_result(data=marshal(favorite, FavoriteDto.model_response), message=messages.MSG_GET_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        pass


    def delete(self, post_id):
        if post_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        current_user = g.current_user
        user_id = current_user.id
        try:
            favorite = PostFavorite.query.filter_by(post_id=post_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message=messages.ERR_NOT_FOUND)
                
            db.session.delete(favorite)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = PostFavorite()
            
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'post_id' in data:
            try:
                favorite.post_id = int(data['post_id'])
            except Exception as e:
                print(e.__str__())
                pass

        return favorite
