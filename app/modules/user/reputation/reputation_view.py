#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.user.reputation.reputation_controller import ReputationController
from app.modules.user.reputation.reputation_dto import ReputationDto
from common.utils.decorator import admin_token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ReputationDto.api
user_reputation_request_parser = ReputationDto.model_user_reputation_request_parser
user_reputation_response = ReputationDto.model_user_reputation_response



@api.route('/all/reputation')
@api.expect(user_reputation_request_parser)
class UserReputationAll(Resource):
    @api.response(code=200, model=user_reputation_response, description='Model for user title response.')
    def get(self):
        """ Search all reputation that satisfy conditions"""

        args = user_reputation_request_parser.parse_args()
        controller = ReputationController()
        return controller.get(args=args)


@api.deprecated
@api.route('/update_all')
class UpdateAllReputation(Resource):
    @admin_token_required()
    def post(self):
        """Update reputation table """

        controller = ReputationController()
        return controller.update_all()
