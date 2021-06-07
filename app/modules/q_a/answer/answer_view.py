#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.answer_controller import AnswerController
from app.modules.q_a.answer.answer_dto import AnswerDto
from common.cache import cache
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerDto.api
answer_upload_parser = AnswerDto.upload_parser
answer_request = AnswerDto.model_request
answer_response = AnswerDto.model_response
get_parser = AnswerDto.get_parser


def get_article_proposal_key_prefix():
    return '{}{}'.format('get.article.proposals', request.view_args['id'])

    
@api.route('/<int:id>/file')
@api.doc(params={'id': 'The answer ID'})
class AnswerFile(Resource):
    @token_required
    @api.expect(answer_upload_parser)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def post(self, id):
        """Create new answer with files (video/audio)"""

        controller = AnswerController()
        return controller.create_with_file(object_id=id)

@api.route('')
class AnswerList(Resource):
    @api.expect(get_parser)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def get(self):
        """Get the list of answers"""

        args = get_parser.parse_args()
        controller = AnswerController()
        return controller.get(args=args)

    @token_required
    @api.expect(answer_request)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def post(self):
        """Create new answer"""

        data = api.payload
        controller = AnswerController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Answer(Resource):
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    @cache.cached(key_prefix=get_article_proposal_key_prefix)
    def get(self, id):
        """Get the answer by answer id"""

        controller = AnswerController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(answer_request)
    @api.response(code=200, model=answer_response, description='Model for answer response.')
    def patch(self, id):
        """Update the existing answer by answer id"""

        data = api.payload
        controller = AnswerController()
        result = controller.update(object_id=id, data=data)
        cache.clear_cache(get_article_proposal_key_prefix())
        return result

    @token_required
    def delete(self, id):
        """Delete existing answer by answer id"""

        controller = AnswerController()
        result = controller.delete(object_id=id)
        cache.clear_cache(get_article_proposal_key_prefix())
        return result
