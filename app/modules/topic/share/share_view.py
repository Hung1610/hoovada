#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.topic.share.share_controller import ShareController
from app.modules.topic.share.share_dto import TopicShareDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = TopicShareDto.api
share_request = TopicShareDto.model_request
share_response = TopicShareDto.model_response


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search shares by user_id')
parser.add_argument('from_date', type=str, required=False, help='Search all shares by start date.')
parser.add_argument('to_date', type=str, required=False, help='Search all shares by finish date.')
parser.add_argument('facebook', type=str, required=False, help='Search all shares to Facebook.')
parser.add_argument('twitter', type=str, required=False, help='Search all shares to Twitter.')
parser.add_argument('zalo', type=str, required=False, help='Search all shares to Zalo.')

@api.route('/<int:topic_id>/share')
class ShareList(Resource):
    @api.expect(parser)
    def get(self, topic_id):
        """
        Search all shares that satisfy conditions.
        """

        args = parser.parse_args()
        controller = ShareController()
        return controller.get(args=args, topic_id=topic_id)
        
    @api.expect(share_request)
    @api.response(code=200, model=share_response, description='The model for share response.')
    def post(self, topic_id):
        """
        Create new share.
        """

        data = api.payload
        controller = ShareController()
        return controller.create(data=data, topic_id=topic_id)


@api.route('/all/share/<int:id>')
class Share(Resource):
    @api.response(code=200, model=share_response, description='The model for share response.')
    def get(self, id):
        """
        Get share by its ID.
        """

        controller = ShareController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(share_request)
    @api.response(code=200, model=share_response, description='The model for share response.')
    def patch(self, id):
        """
        Update existing share by its ID.
        """

        data = api.payload
        controller = ShareController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete share by its ID.
        """
        
        controller = ShareController()
        return controller.delete(object_id=id)