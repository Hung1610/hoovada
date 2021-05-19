#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from app.modules.user.education.education_dto import EducationDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserEducation = db.get_model('UserEducation')


class EducationController(Controller):


    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if user_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
            
        data['user_id'] = user_id

        try:
            education = self._parse_education(data=data, education=None)
            if education.is_current:
                UserEducation.query.filter_by(user_id=user_id).update({'is_current': False}, synchronize_session=False)
            
            db.session.add(education)
            db.session.commit()
            return send_result(data=marshal(education, EducationDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args, user_id=None):
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

        try:
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
            if educations is not None:
                return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(educations, EducationDto.model_response))

        except Exception as e:
            db.session.rollback()
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
            education = UserEducation.query.filter_by(id=object_id).first()
            if education is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            education = self._parse_education(data=data, education=education)
            education.updated_date = datetime.utcnow()
            if education.is_current:
                UserEducation.query.filter(UserEducation.id != education.id, UserEducation.user_id == education.user_id).update({'is_current': False}, synchronize_session=False)
            
            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(education, EducationDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))    

        try:
            education = UserEducation.query.filter_by(id=object_id).first()
            if education is None:
                return send_error(message=messages.ERR_NOT_FOUND)
                
            db.session.delete(education)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


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
            try:
                education.school = data['school']
            except Exception as e:
                print(e.__str__())
                pass

        if 'primary_major' in data:
            try:
                education.primary_major = data['primary_major']
            except Exception as e:
                print(e.__str__())
                pass

        if 'secondary_major' in data:
            try:
                education.secondary_major = data['secondary_major']
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_current' in data:
            try:
                education.is_current = bool(data['is_current'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_visible' in data:
            try:
                education.is_visible = bool(data['is_visible'])
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
