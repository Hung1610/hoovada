#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.user.follow.follow_controller import UserFollowController
# own modules
# from common.decorator import token_required
from app.modules.user.follow.follow_dto import UserFollowDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = UserFollowDto.api
_follow_request = UserFollowDto.model_request
_follow_response = UserFollowDto.model_response
_vote_get_params = UserFollowDto.model_get_parser
_top_users_response = UserFollowDto.top_user_followee_response
_top_user_followee_args_parser = UserFollowDto.top_user_followee_args_parser

@api.route('/all/follow')
class FollowUserAll(Resource):
    @api.expect(_vote_get_params)
    def get(self):
        """
        Search all follow that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = UserFollowController()
        return controller.get(object_id=None, args=args)

@api.route('/all/follow/<int:object_id>/approve')
class FollowUserApprove(Resource):
    def put(self, object_id):
        """
        Approve follow request.
        """
        
        controller = UserFollowController()
        return controller.approve(object_id=object_id)

@api.route('/all/follow/<int:object_id>/disapprove')
class FollowUserDisapprove(Resource):
    def put(self, object_id):
        """
        Disapprove follow request.
        """
        
        controller = UserFollowController()
        return controller.disapprove(object_id=object_id)

@api.route('/<int:user_id>/follow')
class FollowUser(Resource):
    @api.expect(_vote_get_params)
    def get(self, user_id):
        """
        Search all follow that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = UserFollowController()
        return controller.get(object_id=user_id, args=args)

    @token_required
    @api.response(code=200, model=_follow_response, description='The model for follow.')
    def post(self, user_id):
        """
        Create a follow on current user.
        """

        controller = UserFollowController()
        return controller.create(object_id=user_id)

    @token_required
    def delete(self, user_id):
        """
        Delete follow on current user.
        """
        
        controller = UserFollowController()
        return controller.delete(object_id=user_id)


@api.route('/<int:user_id>/follow/top-users')
class FollowRecommendedUsers(Resource):
    @api.expect(_top_user_followee_args_parser)
    @api.response(code=200, model=_top_users_response, description='Model for top users response.')
    def get(self, user_id):
        """ 
        Get recommended users among followers.
        """
        
        args = _top_user_followee_args_parser.parse_args()
        controller = UserFollowController()
        return controller.get_top_users(object_id=user_id, args= args)