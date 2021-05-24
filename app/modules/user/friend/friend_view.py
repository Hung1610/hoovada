#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.friend.friend_controller import UserFriendController
from app.modules.user.friend.friend_dto import UserFriendDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = UserFriendDto.api
_friend_response = UserFriendDto.model_response
_friend_get_params = UserFriendDto.model_get_parser
_top_user_friend_response = UserFriendDto.top_user_friend_response
_top_user_friend_args_parser = UserFriendDto.top_user_friend_args_parser

@api.route('/all/friend')
class FriendUserAll(Resource):
    @api.expect(_friend_get_params)
    def get(self):
        """Get friend requests that satisfy conditions"""

        args = _friend_get_params.parse_args()
        controller = UserFriendController()
        return controller.get(args=args)

@api.route('/all/friend/<int:object_id>/approve')
class FriendUserApprove(Resource):
    def patch(self, object_id):
        """Approve friend request send by user with object_id"""
        
        controller = UserFriendController()
        return controller.approve(object_id=object_id)

@api.route('/all/friend/<int:object_id>/disapprove')
class FriendUserDisapprove(Resource):
    def patch(self, object_id):
        """Disapprove friend request send by user with object_id"""
        
        controller = UserFriendController()
        return controller.disapprove(object_id=object_id)

@api.route('/<int:user_id>/friend')
class FriendUser(Resource):
    @api.deprecated
    @api.expect(_friend_get_params)
    def get(self, user_id):
        """Get all friends of user with user_id"""

        args = _friend_get_params.parse_args()
        args['user_id'] = user_id
        controller = UserFriendController()
        return controller.get(args=args)

    @token_required
    @api.response(code=200, model=_friend_response, description='The model for friend.')
    def post(self, user_id):
        """Create a friend request with user with user_id"""

        controller = UserFriendController()
        return controller.create(object_id=user_id)

    @token_required
    def delete(self, user_id):
        """Delete friend with user with user_id"""
        
        controller = UserFriendController()
        return controller.delete(object_id=user_id)


@api.route('/<int:user_id>/friend/top-users')
class FriendRecommendedUsers(Resource):
    @api.expect(_top_user_friend_args_parser)
    @api.response(code=200, model=_top_user_friend_response, description='Model for top users response.')
    def get(self, user_id):
        """ Get recommended friends"""
        
        args = _top_user_friend_args_parser.parse_args()
        controller = UserFriendController()
        return controller.get_top_users(object_id=user_id, args= args)
