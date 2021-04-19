#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.modules.user.feed.feed_controller import UserFeedController
from app.modules.user.feed.feed_dto import UserFeedDto
from common.utils.decorator import token_required

# own modules
from common.view import Resource

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = UserFeedDto.api
feed_response = UserFeedDto.model_feed_response
feed_all_data_response = UserFeedDto.model_feed_all_data_response
feed_request = UserFeedDto.model_user_feed_request


@api.route('/feed')
@api.expect(feed_request)
@api.response(code=200, model=feed_response, description='Model for feed of user response (only feed IDs).')
class UserGetFeed(Resource):
    @token_required
    def get(self):
        """Get current user's feed with only feed type's data"""

        args = feed_request.parse_args()
        args['get_data'] = False
        controller = UserFeedController()
        return controller.get(args)


@api.route('/feed_all_data')
@api.expect(feed_request)
@api.response(code=200, model=feed_all_data_response, description='Model for feed of user response (all data).')
class UserGetFeedAllData(Resource):
    @token_required
    def get(self):
        """Get current user's feed withn all feed type's data"""

        args = feed_request.parse_args()
        args['get_data'] = True
        controller = UserFeedController()
        return controller.get(args)

