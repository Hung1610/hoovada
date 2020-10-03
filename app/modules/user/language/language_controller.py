#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal
from flask import request

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.user.user import User
from app.modules.user.language.language import UserLanguage
from app.modules.user.language.language_dto import LanguageDto
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class LanguageController(Controller):
    def get(self, args, user_id=None):
        """
        Search languages by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        language_id = None
        if 'language_id' in args:
            try:
                language_id = int(args['language_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = UserLanguage.query
        if user_id is not None:
            query = query.filter(UserLanguage.user_id == user_id)
        if language_id is not None:
            query = query.filter(UserLanguage.language_id == language_id)
            
        languages = query.all()
        if languages is not None and len(languages) > 0:
            return send_result(marshal(languages, LanguageDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any languages.')

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('UserLanguage ID is null')
            language = UserLanguage.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='Could not find language with the ID {}'.format(object_id))
            return send_result(data=marshal(language, LanguageDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get language with the ID {}'.format(object_id))

    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")

        data['user_id'] = user_id

        try:
            language = self._parse_language(data=data, language=None)
            if language.is_default:
                UserLanguage.query.filter_by(user_id=user_id).update({'is_default': False}, synchronize_session=False)
            db.session.add(language)
            db.session.commit()
            return send_result(data=marshal(language, LanguageDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not create language. Error: ' + e.__str__())

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='UserLanguage ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            language = UserLanguage.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='UserLanguage with the ID {} not found.'.format(object_id))

            language = self._parse_language(data=data, language=language)
            language.updated_date = datetime.utcnow()
            if language.is_default:
                UserLanguage.query.filter(UserLanguage.id != language.id, UserLanguage.user_id == language.user_id).update({'is_default': False}, synchronize_session=False)
            db.session.commit()
            return send_result(message='Update successfully', data=marshal(language, LanguageDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update language. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            language = UserLanguage.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='UserLanguage with the ID {} not found.'.format(object_id))
            db.session.delete(language)
            db.session.commit()
            return send_result(message='UserLanguage with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete language with the ID {}.'.format(object_id))

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
            language.level = data['level']
        if 'language_id' in data:
            try:
                language.language_id = int(data['language_id'])
            except Exception as e:
                print(e)
                pass
        if 'is_default' in data:
            try:
                language.is_default = bool(data['is_default'])
            except Exception as e:
                print(e.__str__())
                pass
        return language
