#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.question.share.share_controller import ShareController
from app.modules.q_a.question.share.share_dto import QuestionShareDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = QuestionShareDto.api
SHARE_REQUEST = QuestionShareDto.model_request
SHARE_RESPONSE = QuestionShareDto.model_response
PARSER = QuestionShareDto.parser

@api.route('/<int:question_id>/share')
class ShareList(Resource):
    @api.expect(PARSER)
    @api.response(code=200, model=SHARE_RESPONSE, description='The model for share response.')
    def get(self, question_id):
        """Search all shares that satisfy conditions"""

        args = PARSER.parse_args()
        controller = ShareController()
        return controller.get(args=args, question_id=question_id)
        
    @api.expect(SHARE_REQUEST)
    def post(self, question_id):
        """Create new share using question_id"""

        data = api.payload
        controller = ShareController()
        return controller.create(data=data, question_id=question_id)


@api.route('/all/share/<int:id>')
class Share(Resource):
    @api.response(code=200, model=SHARE_RESPONSE, description='The model for share response.')
    def get(self, id):
        """Get share by its ID"""

        controller = ShareController()
        return controller.get_by_id(object_id=id)