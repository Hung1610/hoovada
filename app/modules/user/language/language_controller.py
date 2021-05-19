#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import marshal

# own modules
from common.db import db
from app.modules.user.language.language_dto import LanguageDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserLanguage = db.get_model('UserLanguage')


class LanguageController(Controller):

    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if user_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))

        data['user_id'] = user_id

        try:
            language = self._parse_language(data=data, language=None)
            db.session.add(language)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(language, LanguageDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def get(self, args, user_id=None):

        language_id = None
        if 'language_id' in args:
            try:
                language_id = int(args['language_id'])
            except Exception as e:
                print(e.__str__())
                pass
        try:
            query = UserLanguage.query
            if user_id is not None:
                query = query.filter(UserLanguage.user_id == user_id)
            if language_id is not None:
                query = query.filter(UserLanguage.language_id == language_id)
                
            languages = query.all()
            return send_result(message=messages.MSG_GET_SUCCESS, data=marshal(languages, LanguageDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self):
        pass


    def update(self, object_id, data):
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            language = UserLanguage.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            language = self._parse_language(data=data, language=language)
            language.updated_date = datetime.utcnow()
            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(language, LanguageDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))    

        try:
            language = UserLanguage.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(language)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_language(self, data, language=None):
        if language is None:
            language = UserLanguage()
        
        if 'user_id' in data:
            try:
                language.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'level' in data:
            try:
                language.level = data['level']
            except Exception as e:
                print(e.__str__())
                pass

        if 'language_id' in data:
            try:
                language.language_id = int(data['language_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_visible' in data:
            try:
                language.is_visible = bool(data['is_visible'])
            except Exception as e:
                print(e.__str__())
                pass

        return language
