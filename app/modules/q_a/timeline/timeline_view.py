#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.timeline.timeline_dto import TimelineDto
from app.modules.q_a.timeline.timeline_controller import TimelineController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = TimelineDto.api
_timeline_dto_request = TimelineDto.timeline_model_request
_timeline_dto_response = TimelineDto.timeline_model_response
_timeline_get_params = TimelineDto.model_get_parser

@api.route('')
class TimelineList(Resource):
    @api.response(code=200, model=_timeline_dto_response, description='Model for timeline response.')
    @api.expect(_timeline_get_params)
    def get(self):
        """
        Get all timelines that satisfy conditions
        """

        args = _timeline_get_params.parse_args()
        controller = TimelineController()
        return controller.get(args=args)


    @token_required
    @api.expect(_timeline_dto_request)
    @api.response(code=200, model=_timeline_dto_response, description='Model for timeline response.')
    def post(self):
        """
        Create new timeline and save to database.
        """

        data = api.payload
        controller = TimelineController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Timeline(Resource):
    @api.response(code=200, model=_timeline_dto_response, description='Model for timeline response.')
    @api.doc(params={'title': 'The name of the topics to search'})
    def get(self, id):
        """
        Get specific timeline by its ID.
        """

        controller = TimelineController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(_timeline_dto_request)
    @api.response(code=200, model=_timeline_dto_response, description='Model for timeline response.')
    def put(self, id):
        """
        Update existing timeline by its ID.
        """

        data = api.payload
        controller = TimelineController()
        return controller.update(object_id=id, data=data, is_put=True)

    @token_required
    @api.expect(_timeline_dto_request)
    @api.response(code=200, model=_timeline_dto_response, description='Model for timeline response.')
    def patch(self, id):
        """
        Update existing timeline by its ID.
        """

        data = api.payload
        controller = TimelineController()
        return controller.update(object_id=id, data=data)

    @admin_token_required
    def delete(self, id_or_slug):
        """
        Delete the timeline by its ID.
        """

        controller = TimelineController()
        return controller.delete(object_id=id_or_slug)