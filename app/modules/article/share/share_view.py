#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.share.share_controller import ShareController
from app.modules.article.share.share_dto import ShareDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = ShareDto.api
share_request = ShareDto.model_request
share_response = ShareDto.model_response

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search shares by user_id')
parser.add_argument('from_date', type=str, required=False, help='Search all shares by start date.')
parser.add_argument('to_date', type=str, required=False, help='Search all shares by finish date.')
parser.add_argument('facebook', type=str, required=False, help='Search all shares to Facebook.')
parser.add_argument('twitter', type=str, required=False, help='Search all shares to Twitter.')
parser.add_argument('zalo', type=str, required=False, help='Search all shares to Zalo.')

@api.route('/<int:article_id>/share')
class ShareList(Resource):
    @api.expect(parser)
    def get(self, article_id):
        """Search all shares that satisfy conditions"""

        args = parser.parse_args()
        controller = ShareController()
        return controller.get(args=args, article_id=article_id)
        
    @api.expect(share_request)
    def post(self, article_id):
        """Create new share"""

        data = api.payload
        controller = ShareController()
        return controller.create(data=data, article_id=article_id)


@api.route('/all/share/<int:id>')
class Share(Resource):
    @api.response(code=200, model=share_response, description='The model for share response.')
    def get(self, id):
        """Get share by its ID"""

        controller = ShareController()
        return controller.get_by_id(object_id=id)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search shares by user_id')

@api.route('/share/get_by_user')
@api.expect(parser)
class ShareSearch(Resource):
    @api.response(code=200, model=share_response, description='Model for share response.')
    def get(self):
        args = parser.parse_args()
        controller = ShareController()
        return controller.get_share_by_user_id(args=args)
