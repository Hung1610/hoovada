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
from app.modules.poll.comment.favorite.favorite_dto import PollCommentFavoriteDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


PollComment = db.get_model('PollComment')
PollCommentFavorite = db.get_model('PollCommentFavorite')


class PollCommentFavoriteController(Controller):
    def get(self, poll_comment_id, args):

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

        query = PollCommentFavorite.query
        if poll_comment_id is not None:
            query = query.filter(PollCommentFavorite.poll_comment_id == poll_comment_id)
        if user_id is not None:
            query = query.filter(PollCommentFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(PollCommentFavorite.poll_comment.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(PollCommentFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PollCommentFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, PollCommentFavoriteDto.model_response), message='Success')
        else:
            return send_result(message='pollComment favorite not found.')

    def create(self, poll_comment_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        comment = PollComment.query.get(poll_comment_id)
        if not comment:
            return send_error(message='Comment not found.')
        if not comment.allow_favorite:
            return send_error(message='Comment does not allow voting.')
        data['user_id'] = current_user.id
        data['poll_comment_id'] = poll_comment_id
        try:
            favorite = PollCommentFavorite.query.filter(PollCommentFavorite.user_id == data['user_id'],
                                             PollCommentFavorite.poll_comment_id == data['poll_comment_id']).first()
            if favorite:
                return send_result(message='This poll_comment is already favorited.')

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='pollComment successfully favorited.',
                               data=marshal(favorite, PollCommentFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to favorite poll_comment.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Please provide poll_comment favorite id.')
        favorite = PollCommentFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='pollComment favorite not found.')
        else:
            return send_result(data=marshal(favorite, PollCommentFavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, poll_comment_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = PollCommentFavorite.query.filter_by(poll_comment_id=poll_comment_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message='PollComment favorite not found.')
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='PollComment favorite deleted successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete poll_comment favorite.')

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = PollCommentFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'poll_comment_id' in data:
            try:
                favorite.poll_comment_id = int(data['poll_comment_id'])
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
