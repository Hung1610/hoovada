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
from app.modules.q_a.post.comment.favorite.favorite_dto import \
    PostCommentFavoriteDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


PostComment = db.get_model('PostComment')
PostCommentFavorite = db.get_model('PostCommentFavorite')


class PostCommentFavoriteController(Controller):
    def get(self, post_comment_id, args):

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

        query = PostCommentFavorite.query
        if post_comment_id is not None:
            query = query.filter(PostCommentFavorite.post_comment_id == post_comment_id)
        if user_id is not None:
            query = query.filter(PostCommentFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(PostCommentFavorite.post_comment.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(PostCommentFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PostCommentFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, PostCommentFavoriteDto.model_response), message='Success')
        else:
            return send_result(message='postComment favorite not found.')

    def create(self, post_comment_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        comment = PostComment.query.get(post_comment_id)
        if not comment:
            return send_error(message='Comment not found.')
        if not comment.allow_favorite:
            return send_error(message='Comment does not allow voting.')
        data['user_id'] = current_user.id
        data['post_comment_id'] = post_comment_id
        try:
            favorite = PostCommentFavorite.query.filter(PostCommentFavorite.user_id == data['user_id'],
                                             PostCommentFavorite.post_comment_id == data['post_comment_id']).first()
            if favorite:
                return send_result(message='This post_comment is already favorited.')

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='postComment successfully favorited.',
                               data=marshal(favorite, PostCommentFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to favorite post_comment.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Please provide post_comment favorite id.')
        favorite = PostCommentFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='postComment favorite not found.')
        else:
            return send_result(data=marshal(favorite, PostCommentFavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, post_comment_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = PostCommentFavorite.query.filter_by(post_comment_id=post_comment_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message='PostComment favorite not found.')
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='PostComment favorite deleted successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete post_comment favorite.')

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = PostCommentFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'post_comment_id' in data:
            try:
                favorite.post_comment_id = int(data['post_comment_id'])
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
