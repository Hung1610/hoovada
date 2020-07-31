#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.q_a.share.share_dto import ShareDto
from app.modules.q_a.share.share_controller import ShareController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = ShareDto.api
share_request = ShareDto.model_request
share_response = ShareDto.model_response


@api.route('')
class ShareList(Resource):
    # @admin_token_required
    # @api.marshal_list_with(share_response)
    # def get(self):
    #     '''
    #     Get list of shares from database.
    #
    #     :return: The list of shares.
    #     '''
    #     controller = ShareController()
    #     return controller.get()

    #@token_required
    @api.expect(share_request)
    @api.response(code=200, model=share_response, description='The model for share response.')
    def post(self):
        '''
        Create new share.

        :return: The new share if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = ShareController()
        return controller.create(data=data)


@api.route('/detail')
class Share(Resource):
    @token_required
    @api.param(name='id', description='The ID of share')
    @api.response(code=200, model=share_response, description='The model for share response.')
    def get(self, id):
        '''
        Get share by its ID.

        :param id: The ID of the share.

        :return: The share with the specific ID.
        '''
        controller = ShareController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(share_request)
    @api.param(name='id', description='The share ID')
    @api.response(code=200, model=share_response, description='The model for share response.')
    def put(self, id):
        '''
        Update existing share by its ID.

        :param id: The ID of the share which need to be updated.

        :return: The updated share if success and null vice versa.
        '''
        data = api.payload
        controller = ShareController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete share by its ID.

        :param id: The ID of the share.

        :return:
        '''
        controller = ShareController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search shares by user_id')
parser.add_argument('question_id', type=str, required=False, help='Search all shares by question_id.')
parser.add_argument('answer_id', type=str, required=False, help='Search all shares by answer_id.')
parser.add_argument('from_date', type=str, required=False, help='Search all shares by start date.')
parser.add_argument('to_date', type=str, required=False, help='Search all shares by finish date.')
parser.add_argument('facebook', type=str, required=False, help='Search all shares to Facebook.')
parser.add_argument('twitter', type=str, required=False, help='Search all shares to Twitter.')
parser.add_argument('zalo', type=str, required=False, help='Search all shares to Zalo.')
parser.add_argument('anonymous', type=str, required=False, help='Search all shares by anonymous.')


@api.route('/search')
@api.expect(parser)
class ShareSearch(Resource):
    @token_required
    @api.response(code=200, model=share_response, description='The model for share response.')
    def get(self):
        """
        Search all shares that satisfy conditions.
        ---------------------

        :user_id: Search shares by user_id

        :question_id: Search all shares by question ID.

        :answer_id: Search shares by answer ID.

        :

        :return: List of comments.
        """
        args = parser.parse_args()
        controller = ShareController()
        return controller.search(args=args)
