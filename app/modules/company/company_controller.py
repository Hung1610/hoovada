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
from common.es import get_model
from common.utils.types import UserRole
from common.cache import cache
from common.controllers.controller import Controller
from common.enum import CompanyStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from app.modules.company.company_dto import CompanyDto
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Company = db.get_model('Company')

class CompanyController(Controller):
    query_classname = 'Company'

    def _parse_company(self, data, company=None):
        if company is None:
            company = Company()

        if 'display_name' in data:
            try:
                company.display_name = data['display_name']
            except Exception as e:
                print(e.__str__())
                pass            

        if 'website_url' in data:
            try:
                company.website_url = data['website_url']
            except Exception as e:
                print(e.__str__())
                pass
        if 'email' in data:
            try:
                company.email = data['email']
            except Exception as e:
                print(e.__str__())
                pass
        if 'phone_number' in data:
            try:
                company.phone_number = data['phone_number']
            except Exception as e:
                print(e.__str__())
                pass
        if 'logo_url' in data:
            try:
                company.logo_url = data['logo_url']
            except Exception as e:
                print(e.__str__())
                pass
        if 'description' in data:
            try:
                company.description = data['description']
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            try:
                company.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass
        return company

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'display_name' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('display_name'))

        if not 'email' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email'))

        if not 'phone_number' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('phone_number'))
        try:     
            # Handling user
            current_user = g.current_user
            data['user_id'] = current_user.id

            # Check if company already exists
            company = Company.query.filter(Company.display_name  == data['display_name']).first()
            if company is not None:
                return send_error(message=messages.ERR_ALREADY_EXISTS)   

            company = self._parse_company(data=data, company=None) 
            company.created_date = datetime.utcnow()
            company.updated_date = datetime.utcnow()
            company.status = CompanyStatusEnum.submitted.name
            db.session.add(company)
            db.session.commit()
            # response data
            result = company._asdict()
            
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, CompanyDto.model_company_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
    
    def update(self, object_id, data):
        try:
            if 'status' in data:
                return send_error(message=messages.ERR_NOT_ALLOWED_PARAMS.format('status'))
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Company ID"))

            if data is None or not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
            company = Company.query.filter_by(id=object_id).first()
            if company is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            current_user = g.current_user
            if company.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            company = self._parse_company(data=data, company=company)       
            company.updated_date = datetime.utcnow()
            db.session.commit()
            result = company._asdict()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CompanyDto.model_company_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    
    def update_status(self, object_id, data):
        try:
            if not UserRole.is_admin(g.current_user.admin):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            if not 'status' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Company status"))
            company_status = None
            if data['status'] == 'submitted':
                company_status = CompanyStatusEnum.submitted.name
            if data['status'] == 'approved':
                company_status = CompanyStatusEnum.approved.name
            if data['status'] == 'rejected':
                company_status = CompanyStatusEnum.rejected.name
            if data['status'] == 'deactivated':
                company_status = CompanyStatusEnum.deactivated.name
            if not company_status:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("A valid company status (submitted,approved,rejected,deactivated)"))
            company = Company.query.filter_by(id=object_id).first()
            if company is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            company.status = company_status
            db.session.commit()
            result = company._asdict()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CompanyDto.model_company_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        company = Company.query.filter_by(id=object_id).first()
        
        if company is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        result = company._asdict()
        return send_result(data=marshal(result, CompanyDto.model_company_response), message=messages.MSG_GET_SUCCESS)
    
    def delete(self, object_id):
        try:
            company = Company.query.filter_by(id=object_id).first()
            if company is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if company.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(company)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
    
    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            # get user information for each answer.
            results = []
            for company in res.get('data'):
                result = company._asdict()
                results.append(result)
            res['data'] = marshal(results, CompanyDto.model_company_response)
            return res, code
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
        