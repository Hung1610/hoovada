#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.user.reputation.reputation_controller import \
    ReputationController
# own modules
from app.modules.user.reputation.reputation_dto import ReputationDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ReputationDto.api
reputation_request = ReputationDto.model_request
user_reputation_response = ReputationDto.user_reputation_response


parser = reqparse.RequestParser()
parser.add_argument('topic_id', type=int, required=False, help='Search reputation by topic_id')
parser.add_argument('user_id', type=int, required=False, help='Search reputation by topic_id')

@api.route('/search')
@api.expect(parser)
class UserReputationSearch(Resource):
    # @token_required
    @api.response(code=200, model=user_reputation_response, description='Model for user title response.')
    def get(self):
        """ 
        Search all reputation that satisfy conditions.
        """

        args = parser.parse_args()
        controller = ReputationController()
        return controller.search(args=args)


@api.route('/update_all')
class UpdateAllReputation(Resource):
    # @admin_token_required()
    def post(self):
        """
        Update Slug for articles in DB
        """

        controller = ReputationController()
        return controller.update_all()
