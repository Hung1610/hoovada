#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from common.models.user import User
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.modules.user.location.location_dto import LocationDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserLocation = db.get_model('UserLocation')


class LocationController(Controller):

    def create(self, data, user_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if user_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        data['user_id'] = user_id

        try:
            location = self._parse_location(data=data, location=None)
            if location.is_current:
                UserLocation.query.filter_by(user_id=user_id).update({'is_current': False}, synchronize_session=False)
            db.session.add(location)
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(location, LocationDto.model_response))

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args, user_id=None):

        location_detail, is_current = None, None
        if 'location_detail' in args:
            try:
                location_detail = args['location_detail']
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_current' in args:
            try:
                is_current = args['is_current']
            except Exception as e:
                print(e.__str__())
                pass

        try:
            query = UserLocation.query

            query = query.join(User, isouter=True)\
                .filter((UserLocation.user == None) | (User.is_deactivated == False))
                
            if g.current_user:
                query = query.filter((User.is_private == False) | (User.id == g.current_user.id))
            else:
                query = query.filter((User.is_private == False))

            if user_id is not None:
                query = query.filter(UserLocation.user_id == user_id)
            
            if location_detail is not None:
                query = query.filter(UserLocation.location_detail == location_detail)

            if is_current is not None:
                query = query.filter(UserLocation.is_current == is_current)
                
            locations = query.all()
            return send_result(message=messages.MSG_GET_SUCCESS, data=marshal(locations, LocationDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self):
        pass


    def update(self, data, object_id):
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            location = UserLocation.query.filter_by(id=object_id).first()
            if location is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            location = self._parse_location(data=data, location=location)
            location.updated_date = datetime.utcnow()
            if location.is_current:
                UserLocation.query.filter(UserLocation.id != location.id, UserLocation.user_id == location.user_id).update({'is_current': False}, synchronize_session=False)
            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(location, LocationDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))   

        try:
            location = UserLocation.query.filter_by(id=object_id).first()
            if location is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(location)
            db.session.commit()

            return send_result(message=messages.MSG_DELETE_SUCCESS)
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def _parse_location(self, data, location=None):
        if location is None:
            location = UserLocation()
        
        if 'user_id' in data:
            try:
                location.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'location_detail' in data:
            try:
                location.location_detail = data['location_detail']
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_current' in data:
            try:
                location.is_current = bool(data['is_current'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_visible' in data:
            try:
                location.is_visible = bool(data['is_visible'])
            except Exception as e:
                print(e.__str__())

        if 'start_year' in data:
            try:
                location.start_year = int(data['start_year'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'end_year' in data:
            try:
                location.end_year = int(data['end_year'])
            except Exception as e:
                print(e.__str__())
                pass

        return location
