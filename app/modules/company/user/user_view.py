#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource

# own modules
from app.modules.company.user.user_controller import CompanyUserController
from app.modules.company.user.user_dto import CompanyUserDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = CompanyUserDto.api
model_company_user_response = CompanyUserDto.model_company_user_response
get_list_request_parser = CompanyUserDto.get_list_request_parser
update_status_request_parser = CompanyUserDto.update_status_request_parser

@api.route('/<int:company_id>/user')
class CompanyUserList(Resource):
    @token_required
    @api.response(code=200, model=model_company_user_response, description='Model for company user response.')
    def post(self, company_id):
        """Add a user to a company"""

        controller = CompanyUserController()
        return controller.create(object_id=company_id)
    
    @token_required
    @api.response(code=200, model=model_company_user_response, description='Model for company user response.')
    def get(self, company_id):
        """Get the list of users who joined the company"""

        args = get_list_request_parser.parse_args()
        controller = CompanyUserController()
        return controller.get(company_id=company_id, args=args)    

@api.route('/all/user/<int:id>')
class CompanyUser(Resource):
    @token_required
    @api.response(code=200, model=model_company_user_response, description='Model for company user response.')
    @api.expect(update_status_request_parser)
    def patch(self, id):
        """Update status of a CompanyUser. You must be admin or the owner of the company to perform this action"""

        args = update_status_request_parser.parse_args()
        controller = CompanyUserController()
        return controller.update(object_id=id, data=args)

    @token_required
    def delete(self, id):
        """Delete existing company user by id"""

        controller = CompanyUserController()
        result = controller.delete(object_id=id)
        return result
