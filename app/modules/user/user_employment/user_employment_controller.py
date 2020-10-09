#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal
import dateutil.parser

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.user.user_employment.user_employment import UserEmployment
from app.modules.user.user_employment.user_employment_dto import UserEmploymentDto
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserEmploymentController(Controller):
    
    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Tham số truyền vào không đúng định dạng.')
        user_id, is_current = None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'is_current' in args:
            try:
                is_current = int(args['is_current'])
            except Exception as e:
                print(e.__str__())
                pass
        if user_id is None :
            return send_error(message='Vui lòng nhập tham số để tìm kiếm.')
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
        return send_result(marshal(results, UserEmploymentDto.model_response), message='Success')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message='Dữ liệu không đúng định dạng.')
        if not 'user_id' in data:
            return send_error(message='Thông tin người dùng không được để trống.')
        if not 'position' in data:
            return send_error(message='Chức vụ không được để trống.')
        if not 'company' in data:
            return send_error(message='Công ty không được để trống.')
        try:
            user_employment = UserEmployment()
            user_employment.user_id = data['user_id']
            user_employment.position = data['position']
            user_employment.company = data['company']
            user_employment.start_year = data['start_year']
            user_employment.end_year = data['end_year']
            user_employment.is_current = data['is_current']
            user_employment.created_date = datetime.utcnow()
            db.session.add(user_employment)
            db.session.commit()

            # if is_default == true cac employment khac cua user cap nhat is_default == false
            UserEmployment.query.filter(UserEmployment.id != user_employment.id,UserEmployment.user_id == data['user_id'])\
                .update({UserEmployment.is_current: 0}, synchronize_session=False)
            db.session.commit()
            return send_result(message='Thông tin nghề nghiệp đã được tạo thành công.',data=marshal(user_employment, UserEmploymentDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Không thể tạo thông tin nghề nghiệp. Kiểm tra lại dữ liệu.')

    def get(self):
        pass

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('UserEmployment ID is null')
            employment = UserEmployment.query.filter_by(id=object_id).first()
            if employment is None:
                return send_error(message='Could not find employment with the ID {}'.format(object_id))
            return send_result(data=marshal(employment, UserEmploymentDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get employment with the ID {}'.format(object_id))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='UserEmployment ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            employment = UserEmployment.query.filter_by(id=object_id).first()
            if employment is None:
                return send_error(message='UserEmployment with the ID {} not found.'.format(object_id))

            employment = self._parse_employment(data=data, employment=employment)
            employment.updated_date = datetime.utcnow()
            db.session.commit()

            # if is_current == true cac employment khac cua user cap nhat is_current == false
            UserEmployment.query.filter(UserEmployment.id != employment.id,UserEmployment.user_id == data['user_id'])\
                .update({UserEmployment.is_current: 0})

            db.session.commit()
            return send_result(message='Update successfully', data=marshal(employment, UserEmploymentDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update employment. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            employment = UserEmployment.query.filter_by(id=object_id).first()
            if employment is None:
                return send_error(message='UserEmployment with the ID {} not found.'.format(object_id))
            db.session.delete(employment)
            db.session.commit()
            return send_result(message='UserEmployment with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete employment with the ID {}.'.format(object_id))

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
            if 'is_currently_work' in data:  
                pass
                try:
                    employment.is_currently_work = bool(data['is_currently_work'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if 'is_current' in data:  
                pass
                try:
                    employment.is_current = bool(data['is_current'])
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