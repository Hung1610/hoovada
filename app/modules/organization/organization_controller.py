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
from common.enum import OrganizationStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from app.modules.organization.organization_dto import OrganizationDto
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

Organization = db.get_model('Organization')

class OrganizationController(Controller):
    query_classname = 'Organization'

    def _parse_organization(self, data, organization=None):
        if organization is None:
            organization = Organization()

        if 'display_name' in data:
            try:
                organization.display_name = data['display_name']
            except Exception as e:
                print(e.__str__())
                pass            

        if 'website_url' in data:
            try:
                organization.website_url = data['website_url']
            except Exception as e:
                print(e.__str__())
                pass
        if 'email' in data:
            try:
                organization.email = data['email']
            except Exception as e:
                print(e.__str__())
                pass
        if 'phone_number' in data:
            try:
                organization.phone_number = data['phone_number']
            except Exception as e:
                print(e.__str__())
                pass
        if 'logo_url' in data:
            try:
                organization.logo_url = data['logo_url']
            except Exception as e:
                print(e.__str__())
                pass
        if 'description' in data:
            try:
                organization.description = data['description']
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            try:
                organization.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass
        return organization

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

            # Check if organization already exists
            organization = Organization.query.filter(Organization.display_name  == data['display_name']).first()
            if organization is not None:
                return send_error(message=messages.ERR_ALREADY_EXISTS)   

            organization = self._parse_organization(data=data, organization=None) 
            organization.created_date = datetime.utcnow()
            organization.updated_date = datetime.utcnow()
            organization.status = OrganizationStatusEnum.submitted.name
            db.session.add(organization)
            db.session.commit()
            # response data
            result = organization._asdict()
            
            return send_result( data=marshal(result, OrganizationDto.model_organization_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
    
    def update(self, object_id, data):
        try:
            if 'status' in data:
                return send_error(message=messages.ERR_NOT_ALLOWED_PARAMS.format('status'))
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Organization ID"))

            if data is None or not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
            organization = Organization.query.filter_by(id=object_id).first()
            if organization is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            current_user = g.current_user
            if organization.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            organization = self._parse_organization(data=data, organization=organization)       
            organization.updated_date = datetime.utcnow()
            db.session.commit()
            result = organization._asdict()
            return send_result(data=marshal(result, OrganizationDto.model_organization_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    
    def update_status(self, object_id, data):
        try:
            if not UserRole.is_admin(g.current_user.admin):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            if not 'status' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Organization status"))
            organization_status = None
            if data['status'] == 'submitted':
                organization_status = OrganizationStatusEnum.submitted.name
            if data['status'] == 'approved':
                organization_status = OrganizationStatusEnum.approved.name
            if data['status'] == 'rejected':
                organization_status = OrganizationStatusEnum.rejected.name
            if data['status'] == 'deactivated':
                organization_status = OrganizationStatusEnum.deactivated.name
            if not organization_status:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("A valid organization status (submitted,approved,rejected,deactivated)"))
            organization = Organization.query.filter_by(id=object_id).first()
            if organization is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            organization.status = organization_status
            db.session.commit()
            result = organization._asdict()
            return send_result(data=marshal(result, OrganizationDto.model_organization_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        organization = Organization.query.filter_by(id=object_id).first()
        
        if organization is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        result = organization._asdict()
        return send_result(data=marshal(result, OrganizationDto.model_organization_response))
    
    def delete(self, object_id):
        try:
            organization = Organization.query.filter_by(id=object_id).first()
            if organization is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if organization.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(organization)
            db.session.commit()
            return send_result()
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
            for organization in res.get('data'):
                result = organization._asdict()
                results.append(result)
            res['data'] = marshal(results, OrganizationDto.model_organization_response)
            return res, code
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
        