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
from app.modules.q_a.question.comment.comment import QuestionComment
from app.modules.q_a.question.comment.favorite.favorite import QuestionCommentFavorite
from app.modules.q_a.question.comment.favorite.favorite_dto import QuestionCommentFavoriteDto
from app.modules.user.user import User
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionCommentFavoriteController(Controller):
    def get(self, question_comment_id, args):
        '''
        Get/Search favorites.

        Args:
             The dictionary-like parameters.

        Returns:
        '''
        
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

        query = QuestionCommentFavorite.query
        if question_comment_id is not None:
            query = query.filter(QuestionCommentFavorite.question_comment_id == question_comment_id)
        if user_id is not None:
            query = query.filter(QuestionCommentFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(QuestionCommentFavorite.question_comment.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(QuestionCommentFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(QuestionCommentFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, QuestionCommentFavoriteDto.model_response), message='Success')
        else:
            return send_result(message='QuestionComment favorite not found.')

    def create(self, question_comment_id):
        data = {}
        current_user, _ = AuthController.get_logged_user(request)
        data['user_id'] = current_user.id
        data['question_comment_id'] = question_comment_id
        try:
            favorite = QuestionCommentFavorite.query.filter(QuestionCommentFavorite.user_id == data['user_id'],
                                             QuestionCommentFavorite.question_comment_id == data['question_comment_id']).first()
            if favorite:
                return send_result(message='This question_comment is already favorited.')

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='QuestionComment successfully favorited.',
                               data=marshal(favorite, QuestionCommentFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to favorite question_comment.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Please provide question_comment favorite id.')
        favorite = QuestionCommentFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='QuestionComment favorite not found.')
        else:
            return send_result(data=marshal(favorite, QuestionCommentFavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, question_comment_id):
        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = QuestionCommentFavorite.query.filter_by(question_comment_id=question_comment_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message='QuestionComment favorite not found.')
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='QuestionComment favorite deleted successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete question_comment favorite.')

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = QuestionCommentFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_comment_id' in data:
            try:
                favorite.question_comment_id = int(data['question_comment_id'])
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
