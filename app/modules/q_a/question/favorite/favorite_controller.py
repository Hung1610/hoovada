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
from app.constants import messages
from app.modules.q_a.question.favorite.favorite_dto import QuestionFavoriteDto
from common.controllers.controller import Controller
from common.models import Answer, Question, QuestionFavorite, User
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType, UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionFavoriteController(Controller):
    def get(self, question_id, args):
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

        query = QuestionFavorite.query
        if question_id is not None:
            query = query.filter(QuestionFavorite.question_id == question_id)
        if user_id is not None:
            query = query.filter(QuestionFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(QuestionFavorite.question.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(QuestionFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(QuestionFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, QuestionFavoriteDto.model_response), message='Success')
        else:
            return send_result(message='Question favorite not found.')

    def create(self, question_id):
        current_user, _ = current_app.get_logged_user(request)
        # Check is admin or has permission
        if not (UserRole.is_admin(current_user.admin)
                or has_permission(current_user.id, PermissionType.QUESTION_FAVORITE)):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        data['question_id'] = question_id
        try:
            favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == data['user_id'],
                                             QuestionFavorite.question_id == data['question_id']).first()
            if favorite:
                return send_result(message='This question is already favorited.')

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='Question successfully favorited.',
                               data=marshal(favorite, QuestionFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to favorite question.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Please provide question favorite id.')
        favorite = QuestionFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='Question favorite not found.')
        else:
            return send_result(data=marshal(favorite, QuestionFavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, question_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = QuestionFavorite.query.filter_by(question_id=question_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message='Question favorite not found.')
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='Question favorite deleted successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete question favorite.')

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = QuestionFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in data:
            try:
                favorite.question_id = int(data['question_id'])
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
