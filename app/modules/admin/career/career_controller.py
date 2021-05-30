#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import dateutil.parser
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from app.modules.admin.career.career_dto import CareerDto
from app.constants import messages
from common.db import db
from common.models.user import User
from common.models.career import Career
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CareerController(Controller):
    query_classname = 'Career'
    special_filtering_fields = ['from_date', 'to_date', 'title']
    allowed_ordering_fields = ['created_date', 'updated_date']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'title' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))

        if not 'description' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('description'))

        # Handling user
        current_user = g.current_user
        data['user_id'] = current_user.id

        # handling title
        data['title'] = data['title'].strip().capitalize()
        career = Career.query.filter(Career.title == data['title']).first()
        if career:
            return send_error(message=messages.ERR_ALREADY_EXISTS)

        career = self._parse_career(data=data, career=None)
        try:
            db.session.add(career)
            db.session.commit()

            result = career._asdict()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, CareerDto.model_career_response))

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_query(self):
        query = super().get_query().filter(db.or_(Career.user == None, User.is_deactivated != True))
        return query


    def apply_filtering(self, query, params):
        try:
            query = super().apply_filtering(query, params)
            if params.get('title'):
                query = query.filter(Career.title.like(params.get('title')))

            if params.get('from_date'):
                query = query.filter(Career.created_date >= dateutil.parser.isoparse(params.get('from_date')))

            if params.get('to_date'):
                query = query.filter(Career.created_date <= dateutil.parser.isoparse(params.get('to_date')))
            return query
        except Exception as e:
            print(e.__str__())
            raise e


    def get(self, args):

        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            careers = res.get('data')

            results = []
            for career in careers:
                result = career._asdict()
                results.append(result)

            res['data'] = marshal(results, CareerDto.model_career_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(str(e)))


    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('Career Id'))
            if object_id.isdigit():
                career = Career.query.filter_by(id=object_id).first()
            else:
                career = Career.query.filter_by(slug=object_id).first()

            if career is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.commit()
            result = career._asdict()
            
            return send_result(data=marshal(result, CareerDto.model_career_response), message='Success')

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(str(e)))


    def update(self, object_id, data):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('Career Id'))

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            career = Career.query.filter_by(id=object_id).first()
        else:
            career = Career.query.filter_by(slug=object_id).first()

        if career is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        career = self._parse_career(data=data, career=career)
        try:
            career.updated_date = datetime.utcnow()
            db.session.commit()

            result = career._asdict()

            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CareerDto.model_career_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(str(e)))


    def delete(self, object_id):
        try:
            if object_id.isdigit():
                career = Career.query.filter_by(id=object_id).first()
            else:
                career = Career.query.filter_by(slug=object_id).first()

            if career is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(career)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(str(e)))


    def _parse_career(self, data, career=None):
        if career is None:
            career = Career()
        career._from_dict(data)

        return career
