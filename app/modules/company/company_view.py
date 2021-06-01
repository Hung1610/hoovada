#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource

# own modules
from app.modules.company.company_controller import CompanyController
from app.modules.company.company_dto import CompanyDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = CompanyDto.api
post_request_parser = CompanyDto.post_request_parser
model_company_response = CompanyDto.model_company_response
get_list_request_parser = CompanyDto.get_list_request_parser
update_status_request_parser = CompanyDto.update_status_request_parser


@api.route('')
class CompanyList(Resource):
    @token_required
    @api.expect(post_request_parser)
    @api.response(code=200, model=model_company_response, description='Model for company response.')
    def post(self):
        """ Create new company"""

        data = api.payload
        controller = CompanyController()
        return controller.create(data=data)

    @token_required
    @api.expect(get_list_request_parser)
    @api.response(code=200, model=model_company_response, description='Model for company response.')
    def get(self):
        """Get the list of companies"""

        args = get_list_request_parser.parse_args()
        controller = CompanyController()
        return controller.get(args=args)

@api.route('/<int:id>')
class Company(Resource):
    @token_required
    @api.response(code=200, model=model_company_response, description='Model for company response.')
    def get(self, id):
        """Get a company"""

        controller = CompanyController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(post_request_parser)
    @api.response(code=200, model=model_company_response, description='Model for company response.')
    def patch(self, id):
        """Update the existing company by company id"""

        data = api.payload
        controller = CompanyController()
        result = controller.update(object_id=id, data=data)
        return result

    @token_required
    def delete(self, id):
        """Delete existing company by company id"""

        controller = CompanyController()
        result = controller.delete(object_id=id)
        return result

@api.route('/<int:id>/status')
class Company(Resource):
    @token_required
    @api.expect(update_status_request_parser)
    @api.response(code=200, model=model_company_response, description='Model for company response.')
    def patch(self, id):
        """Update the status of company by company id. You must be admin to perform this action"""

        data = api.payload
        controller = CompanyController()
        result = controller.update_status(object_id=id, data=data)
        return result    