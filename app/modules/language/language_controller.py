#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal

from app.app import db
from app.modules.language.language_dto import LanguageDto
# own modules
from common.controllers.controller import Controller
from common.models import Language
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class LanguageController(Controller):

    def create_languages(self):
        fixed_languages = [{"code":"vi-VN", "name":"Vietnamese"},
                        {"code":"en-US", "name":"English US"}, ]

        try:
            for language_insert in fixed_languages:
                language = Language.query.filter(Language.name == language_insert["name"]).first()
                if not language:  # the language does not exist
                    language = Language(name=language_insert["name"], code=language_insert["code"])
                    db.session.add(language)
                    db.session.commit()
        except Exception as e:
            print(e.__str__())
            pass
        return self.get({})

    def get(self, args):
        if not isinstance(args, dict):
            return send_error(message='Could not parse the params')
        name, code = None, None
        if 'name' in args:
            name = args['name']
        if 'code' in args:
            code = args['code']

        query = db.session.query(Language)
        if name is not None and not str(name).strip().__eq__(''):
            name = '%' + name.strip() + '%'
            query = query.filter(Language.name.like(name))
        if code is not None:
            query = query.filter(Language.code == code)
            
        languages = query.all()
        if languages is not None and len(languages) > 0:
            return send_result(marshal(languages, LanguageDto.model_response), message='Success')
        else:
            return send_error(message='Could not find any languages.')

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('Language ID is null')
            language = Language.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='Could not find language with the ID {}'.format(object_id))
            return send_result(data=marshal(language, LanguageDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get language with the ID {}'.format(object_id))

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")

        try:
            language = self._parse_language(data=data, language=None)
            db.session.add(language)
            db.session.commit()
            return send_result(data=marshal(language, LanguageDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not create language. Error: ' + e.__str__())

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='Language ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            language = Language.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='Language with the ID {} not found.'.format(object_id))

            language = self._parse_language(data=data, language=language)
            language.updated_date = datetime.utcnow()
            db.session.commit()
            return send_result(message='Update successfully', data=marshal(language, LanguageDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update language. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            language = Language.query.filter_by(id=object_id).first()
            if language is None:
                return send_error(message='Language with the ID {} not found.'.format(object_id))
            db.session.delete(language)
            db.session.commit()
            return send_result(message='Language with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete language with the ID {}.'.format(object_id))

    def _parse_language(self, data, language=None):
        if language is None:
            language = Language()
        if 'name' in data:
            language.name = data['name']
        if 'code' in data:
            language.code = data['code']
        if 'description' in data:
            language.description = data['description']
        return language
