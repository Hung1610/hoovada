#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from app.modules.user.user_employment.user_employment_dto import EmploymentDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserEmployment = db.get_model('UserEmployment')


class EmploymentController(Controller):

    def create(self, data, user_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if user_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        data['user_id'] = user_id

        if not 'position' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('position'))
        
        if not 'company' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('company'))

        try:
            user_employment = self._parse_employment(data, employment=None)
            user_employment.created_date = datetime.utcnow()
            db.session.add(user_employment)
            db.session.commit()

            UserEmployment.query.filter(UserEmployment.id != user_employment.id, UserEmployment.user_id == data['user_id'])\
                                .update({UserEmployment.is_current: 0}, synchronize_session=False)

            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(user_employment, EmploymentDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self,  args, user_id=None):

        if 'is_current' in args:
            try:
                is_current = int(args['is_current'])
            except Exception as e:
                print(e.__str__())
                pass
        try:
            query = db.session.query(UserEmployment)

            if user_id is not None:
                query = query.filter(UserEmployment.user_id == user_id)

            if is_current is not None:
                query = query.filter(UserEmployment.is_current == is_current)

            user_employments = query.all()
            results = list()
            for user_employment in user_employments:
                result = user_employment.__dict__
                results.append(result)
                
            return send_result(message=messages.MSG_GET_SUCCESS, data=marshal(results, EmploymentDto.model_response))
            
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        pass


    def update(self, object_id, data):

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            employment = UserEmployment.query.filter_by(id=object_id).first()
            if employment is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            employment = self._parse_employment(data=data, employment=employment)
            employment.updated_date = datetime.utcnow()
            db.session.commit()

            # if is_current == true cac employment khac cua user cap nhat is_current == false
            UserEmployment.query.filter(UserEmployment.id != employment.id,UserEmployment.user_id == data['user_id'])\
                .update({UserEmployment.is_current: 0})

            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(employment, EmploymentDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))        

        try:
            employment = UserEmployment.query.filter_by(id=object_id).first()
            if employment is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(employment)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_employment(self, data, employment=None):
        if employment is None:
            employment = UserEmployment()

        if 'user_id' in data:
            try:
                employment.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'position' in data:
            try:
                employment.position = data['position']
            except Exception as e:
                print(e.__str__())
                pass

        if 'company' in data:
            try:
                employment.company = data['company']
            except Exception as e:
                print(e.__str__())
                pass

        if 'start_year' in data:
            try:
                employment.start_year = int(data['start_year'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'end_year' in data:
            try:
                employment.end_year = int(data['end_year'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_current' in data:  
            try:
                employment.is_current = bool(data['is_current'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_visible' in data:
            try:
                employment.is_visible = bool(data['is_visible'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'created_date' in data:
            try:
                employment.created_date = dateutil.parser.isoparse(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass

        return employment