#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from common.utils.types import UserRole
from common.controllers.controller import Controller
from common.enum import CompanyUserStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from app.modules.company.user.user_dto import CompanyUserDto
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

CompanyUser = db.get_model('CompanyUser')
Company = db.get_model('Company')

class CompanyUserController(Controller):
    query_classname = 'CompanyUser'

    def _parse_company_user(self, data, company_user):
        if company_user is None:
            company_user = CompanyUser()

        if 'user_id' in data:
            try:
                company_user.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass            

        if 'company_id' in data:
            try:
                company_user.company_id = data['company_id']
            except Exception as e:
                print(e.__str__())
                pass
        return company_user     

    def create(self, object_id):
        current_user = g.current_user
        try:
            # Check if company already exists
            company = Company.query.filter(Company.id  == object_id).first()
            if company is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Company', object_id))
            company_user = CompanyUser.query.filter_by(user_id=current_user.id, company_id=company.id).first()
            if company_user is not None:
                return send_error(message=messages.ERR_ALREADY_EXISTS)
            data = {}
            data['user_id'] = current_user.id
            data['company_id'] = company.id
            company_user = self._parse_company_user(data, None)
            company_user.created_date = datetime.utcnow()
            company_user.updated_date = datetime.utcnow()
            company_user.status = CompanyUserStatusEnum.submitted.name
            db.session.add(company_user)
            db.session.commit()
            # response data
            result = company._asdict()
            
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, CompanyUserDto.model_company_user_response))
        
        except Exception as e:
            print(e)
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
    
    def update(self, object_id, data):
        try:
            if not 'status' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('status of CompanyUser'))
            company_user_status = None
            if data['status'] == 'submitted':
                company_user_status = CompanyUserStatusEnum.submitted.name
            if data['status'] == 'approved':
                company_user_status = CompanyUserStatusEnum.approved.name
            if data['status'] == 'rejected':
                company_user_status = CompanyUserStatusEnum.rejected.name
            if data['status'] == 'deactivated':
                company_user_status = CompanyUserStatusEnum.deactivated.name
            if not company_user_status:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("A valid company user status (submitted,approved,rejected,deactivated)"))
            # Check if company_user already exists
            company_user = CompanyUser.query.filter(CompanyUser.id  == object_id).first()
            if company_user is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('CompanyUser', object_id))
            if g.current_user.id != company_user.company.user_id or not UserRole.is_admin(g.current_user.admin):
                return send_error(message=messages.ERR_NOT_AUTHORIZED)
            company_user.updated_date = datetime.utcnow()
            company_user.status = company_user_status
            db.session.commit()
            # response data
            result = company_user._asdict()
            
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CompanyUserDto.model_company_user_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))
    
    def get(self, company_id, args):
        try:
            args['company_id'] = company_id
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            # get user information for each answer.
            results = []
            for company in res.get('data'):
                result = company._asdict()
                results.append(result)
            res['data'] = marshal(results, CompanyUserDto.model_company_user_response)
            return res, code
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
    
    def get_by_id(self, *args, **kwargs):
        return super().get_by_id(*args, **kwargs)
    
    def delete(self, object_id):
        try:
            company_user = CompanyUser.query.filter_by(id=object_id).first()
            if company_user is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if company_user.company.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(company_user)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
