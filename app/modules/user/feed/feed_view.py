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

@api.route('/feed_all_data')
@api.expect(UserFeedDto.model_user_feed_request)
@api.response(code=200, model=UserFeedDto.model_feed_all_data_response, description='Model for feed of user response (all data).')
class UserGetFeedAllData(Resource):
    @token_required
    def get(self):
        """Get current user's feed with all feed type's data"""

        args = UserFeedDto.model_user_feed_request.parse_args()
        args['get_data'] = True
        controller = UserFeedController()
        return controller.get(args)

