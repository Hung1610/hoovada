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
from app.modules.q_a.answer.favorite.favorite_dto import AnswerFavoriteDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Answer = db.get_model('Answer')
AnswerFavorite = db.get_model('AnswerFavorite')
User = db.get_model('User')


class AnswerFavoriteController(Controller):
    def get(self, answer_id, args):
        '''Get/Search favorites.
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

        query = AnswerFavorite.query
        if answer_id is not None:
            query = query.filter(AnswerFavorite.answer_id == answer_id)
        if user_id is not None:
            query = query.filter(AnswerFavorite.user_id == user_id)
        if favorited_user_id is not None:
            query = query.filter(AnswerFavorite.answer.user_id == favorited_user_id)
        if from_date is not None:
            query = query.filter(AnswerFavorite.created_date >= from_date)
        if to_date is not None:
            query = query.filter(AnswerFavorite.created_date <= to_date)
        favorites = query.all()
        if favorites is not None and len(favorites) > 0:
            return send_result(data=marshal(favorites, AnswerFavoriteDto.model_response), message='Success')
        else:
            return send_result(message='Answer favorite not found.')

    def create(self, answer_id):
        data = {}
        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            favorite = AnswerFavorite.query.filter(AnswerFavorite.user_id == data['user_id'],
                                             AnswerFavorite.answer_id == data['answer_id']).first()
            if favorite:
                return send_result(message='This answer is already favorited.')

            favorite = self._parse_favorite(data=data, favorite=None)
            favorite.created_date = datetime.utcnow()
            favorite.updated_date = datetime.utcnow()
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='Answer successfully favorited.',
                               data=marshal(favorite, AnswerFavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to favorite answer.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Please provide answer favorite id.')
        favorite = AnswerFavorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='Answer favorite not found.')
        else:
            return send_result(data=marshal(favorite, AnswerFavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, answer_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            favorite = AnswerFavorite.query.filter_by(answer_id=answer_id, user_id=user_id).first()
            if favorite is None:
                return send_error(message='Answer favorite not found.')
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='Answer favorite deleted successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete answer favorite.')

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = AnswerFavorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
            try:
                favorite.answer_id = int(data['answer_id'])
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
