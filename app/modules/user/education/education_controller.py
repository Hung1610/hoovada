#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from flask import request
# third-party modules
from flask_restx import marshal

# own modules
from app.app import db
from app.modules.auth.auth_controller import AuthController
from app.modules.user.education.education import UserEducation
from app.modules.user.education.education_dto import EducationDto
from common.controllers.controller import Controller
from common.models import User
from common.utils.response import send_error, send_result
from common.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class EducationController(Controller):
    def get(self, args, user_id=None):
        """
        Search educations by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        school, primary_major, secondary_major = None, None, None 
        if 'school' in args:
            try:
                school = args['school']
            except Exception as e:
                print(e.__str__())
                pass
        if 'primary_major' in args:
            try:
                primary_major = args['primary_major']
            except Exception as e:
                print(e.__str__())
                pass
        if 'secondary_major' in args:
            try:
                secondary_major = args['secondary_major']
            except Exception as e:
                print(e.__str__())
                pass

        query = UserEducation.query
        if user_id is not None:
            query = query.filter(UserEducation.user_id == user_id)
        if school is not None:
            query = query.filter(UserEducation.school == school)
        if primary_major is not None:
            query = query.filter(UserEducation.primary_major == primary_major)
        if secondary_major is not None:
            query = query.filter(UserEducation.secondary_major == secondary_major)
            
        educations = query.all()
        if educations is not None and len(educations) > 0:
            return send_result(marshal(educations, EducationDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any educations.')

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('UserEducation ID is null')
            education = UserEducation.query.filter_by(id=object_id).first()
            if education is None:
                return send_error(message='Could not find education with the ID {}'.format(object_id))
            return send_result(data=marshal(education, EducationDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get education with the ID {}'.format(object_id))

    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")

        data['user_id'] = user_id

        try:
            education = self._parse_education(data=data, education=None)
            if education.is_current:
                UserEducation.query.filter_by(user_id=user_id).update({'is_current': False}, synchronize_session=False)
            db.session.add(education)
            db.session.commit()
            return send_result(data=marshal(education, EducationDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not create education. Error: ' + e.__str__())

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='UserEducation ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            education = UserEducation.query.filter_by(id=object_id).first()
            if education is None:
                return send_error(message='UserEducation with the ID {} not found.'.format(object_id))

            education = self._parse_education(data=data, education=education)
            education.updated_date = datetime.utcnow()
            if education.is_current:
                UserEducation.query.filter(UserEducation.id != education.id, UserEducation.user_id == education.user_id).update({'is_current': False}, synchronize_session=False)
            db.session.commit()
            return send_result(message='Update successfully', data=marshal(education, EducationDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update education. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            education = UserEducation.query.filter_by(id=object_id).first()
            if education is None:
                return send_error(message='UserEducation with the ID {} not found.'.format(object_id))
            db.session.delete(education)
            db.session.commit()
            return send_result(message='UserEducation with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete education with the ID {}.'.format(object_id))

    def _parse_education(self, data, education=None):
        if education is None:
            education = UserEducation()
        if 'user_id' in data:
            try:
                education.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'school' in data:
            education.school = data['school']
        if 'primary_major' in data:
            education.primary_major = data['primary_major']
        if 'secondary_major' in data:
            education.secondary_major = data['secondary_major']
        if 'is_current' in data:
            try:
                education.is_current = bool(data['is_current'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'start_year' in data:
            try:
                education.start_year = int(data['start_year'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'end_year' in data:
            try:
                education.end_year = int(data['end_year'])
            except Exception as e:
                print(e.__str__())
                pass
        return education
