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
from app.modules.user.location.location import UserLocation
from app.modules.user.location.location_dto import LocationDto
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class LocationController(Controller):
    def get(self, args, user_id=None):
        """
        Search locations by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        location_detail = None 
        if 'location_detail' in args:
            try:
                location_detail = args['location_detail']
            except Exception as e:
                print(e.__str__())
                pass

        query = UserLocation.query
        if user_id is not None:
            query = query.filter(UserLocation.user_id == user_id)
        if location_detail is not None:
            query = query.filter(UserLocation.location_detail == location_detail)
            
        locations = query.all()
        if locations is not None and len(locations) > 0:
            return send_result(marshal(locations, LocationDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any locations.')

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error('UserLocation ID is null')
            location = UserLocation.query.filter_by(id=object_id).first()
            if location is None:
                return send_error(message='Could not find location with the ID {}'.format(object_id))
            return send_result(data=marshal(location, LocationDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get location with the ID {}'.format(object_id))

    def create(self, user_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")

        data['user_id'] = user_id

        try:
            location = self._parse_location(data=data, location=None)
            if location.is_current:
                UserLocation.query.update({'is_current': False}, synchronize_session=False)
            db.session.add(location)
            db.session.commit()
            return send_result(data=marshal(location, LocationDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not create location. Error: ' + e.__str__())

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='UserLocation ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            location = UserLocation.query.filter_by(id=object_id).first()
            if location is None:
                return send_error(message='UserLocation with the ID {} not found.'.format(object_id))
            if location.is_current:
                UserLocation.query.update({'is_current': False}, synchronize_session=False)

            location = self._parse_location(data=data, location=location)
            location.updated_date = datetime.utcnow()
            db.session.commit()
            return send_result(message='Update successfully', data=marshal(location, LocationDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update location. Error: ' + e.__str__())

    def delete(self, object_id):
        try:
            location = UserLocation.query.filter_by(id=object_id).first()
            if location is None:
                return send_error(message='UserLocation with the ID {} not found.'.format(object_id))
            db.session.delete(location)
            db.session.commit()
            return send_result(message='UserLocation with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete location with the ID {}.'.format(object_id))

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
            location.location_detail = data['location_detail']
        if 'is_current' in data:
            try:
                location.is_current = bool(data['is_current'])
            except Exception as e:
                print(e.__str__())
                pass
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
