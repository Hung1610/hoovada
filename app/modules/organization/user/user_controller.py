
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
from common.enum import OrganizationUserStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from app.modules.organization.user.user_dto import OrganizationUserDto
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

OrganizationUser = db.get_model('OrganizationUser')
Organization = db.get_model('Organization')

class OrganizationUserController(Controller):
    query_classname = 'OrganizationUser'

    def _parse_organization_user(self, data, organization_user):
        if organization_user is None:
            organization_user = OrganizationUser()

        if 'user_id' in data:
            try:
                organization_user.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass            

        if 'organization_id' in data:
            try:
                organization_user.organization_id = data['organization_id']
            except Exception as e:
                print(e.__str__())
                pass
        return organization_user     

    def create(self, object_id):
        current_user = g.current_user
        try:
            # Check if organization already exists
            organization = Organization.query.filter(Organization.id  == object_id).first()
            if organization is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Organization', object_id))
            organization_user = OrganizationUser.query.filter_by(user_id=current_user.id, organization_id=organization.id).first()
            if organization_user is not None:
                return send_error(message=messages.ERR_ALREADY_EXISTS)
            data = {}
            data['user_id'] = current_user.id
            data['organization_id'] = organization.id
            organization_user = self._parse_organization_user(data, None)
            organization_user.created_date = datetime.utcnow()
            organization_user.updated_date = datetime.utcnow()
            organization_user.status = OrganizationUserStatusEnum.submitted.name
            db.session.add(organization_user)
            db.session.commit()
            # response data
            result = organization_user._asdict()
            
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, OrganizationUserDto.model_organization_user_response))
        
        except Exception as e:
            print(e)
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
    
    def update(self, object_id, data):
        try:
            if not 'status' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('status of OrganizationUser'))
            organization_user_status = None
            if data['status'] == 'submitted':
                organization_user_status = OrganizationUserStatusEnum.submitted.name
            if data['status'] == 'approved':
                organization_user_status = OrganizationUserStatusEnum.approved.name
            if data['status'] == 'rejected':
                organization_user_status = OrganizationUserStatusEnum.rejected.name
            if data['status'] == 'deactivated':
                organization_user_status = OrganizationUserStatusEnum.deactivated.name
            if not organization_user_status:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format("A valid organization user status (submitted,approved,rejected,deactivated)"))
            # Check if organization_user already exists
            organization_user = OrganizationUser.query.filter(OrganizationUser.id  == object_id).first()
            if organization_user is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('OrganizationUser', object_id))
            if g.current_user.id != organization_user.organization.user_id or not UserRole.is_admin(g.current_user.admin):
                return send_error(message=messages.ERR_NOT_AUTHORIZED)
            organization_user.updated_date = datetime.utcnow()
            organization_user.status = organization_user_status
            db.session.commit()
            # response data
            result = organization_user._asdict()
            
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, OrganizationUserDto.model_organization_user_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))
    
    def get(self, organization_id, args):
        try:
            args['organization_id'] = organization_id
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            # get user information for each answer.
            results = []
            for organization in res.get('data'):
                result = organization._asdict()
                results.append(result)
            res['data'] = marshal(results, OrganizationUserDto.model_organization_user_response)
            return res, code
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
    
    def get_by_id(self, *args, **kwargs):
        return super().get_by_id(*args, **kwargs)
    
    def delete(self, object_id):
        try:
            organization_user = OrganizationUser.query.filter_by(id=object_id).first()
            if organization_user is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if organization_user.organization.user_id != current_user.id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(organization_user)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))