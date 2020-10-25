#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from common.decorator import token_required
from app.modules.user.friend.friend_dto import UserFriendDto
from app.modules.user.friend.friend_controller import UserFriendController
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = UserFriendDto.api
_friend_request = UserFriendDto.model_request
_friend_response = UserFriendDto.model_response
_vote_get_params = UserFriendDto.model_get_parser
_top_user_friend_response = UserFriendDto.top_user_friend_response
_top_user_friend_args_parser = UserFriendDto.top_user_friend_args_parser

@api.route('/all/friend')
class FriendUserAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """
        Search all friend that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = UserFriendController()
        return controller.get(object_id=None, args=args)

@api.route('/all/friend/<int:object_id>/approve')
class FriendUserApprove(Resource):
    def put(self, object_id):
        """
        Approve friend request.
        """
        
        controller = UserFriendController()
        return controller.approve(object_id=object_id)

@api.route('/all/friend/<int:object_id>/disapprove')
class FriendUserDisapprove(Resource):
    def put(self, object_id):
        """
        Disapprove friend request.
        """
        
        controller = UserFriendController()
        return controller.disapprove(object_id=object_id)

@api.route('/<int:user_id>/friend')
class FriendUser(Resource):
    @api.expect(_vote_get_params)
    def get(self, user_id):
        """
        Search all friend that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = UserFriendController()
        return controller.get(object_id=user_id, args=args)

    @token_required
    @api.response(code=200, model=_friend_response, description='The model for friend.')
    def post(self, user_id):
        """
        Create a friend on current user.
        """

        controller = UserFriendController()
        return controller.create(object_id=user_id)

    @token_required
    def delete(self, user_id):
        """
        Delete friend on current user.
        """
        
        controller = UserFriendController()
        return controller.delete(object_id=user_id)


@api.route('/<int:user_id>/friend/top-users')
class FriendRecommendedUsers(Resource):
    @api.expect(_top_user_friend_args_parser)
    @api.response(code=200, model=_top_user_friend_response, description='Model for top users response.')
    def get(self, user_id):
        """ 
        Get recommended users among friends.
        """
        
        args = _top_user_friend_args_parser.parse_args()
        controller = UserFriendController()
        return controller.get_top_users(object_id=user_id, args= args)
