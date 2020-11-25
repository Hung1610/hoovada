#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AnswerImprovementDto(Dto):
    name = 'answer_improvement'
    api = Namespace(name, description="Answer improvement operations")

    answer_improvement_user = api.model('answer_improvement_user',{
        'id': fields.Integer(readonly=True, description = 'The user ID'),
        'display_name': fields.String(required=True, description = 'The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('answer_improvement_request', {
        'content': fields.String(description='The content of the answer'),
    })

    model_response = api.model('answer_improvement_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the answer'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date answer was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date answer was updated'),
        'content': fields.String(description='The content of the answer'),
        'user':fields.Nested(answer_improvement_user, description='The information of the user'),
        'answer_id': fields.Integer(default=0, description='The ID of the answer_id'),
        'vote_score': fields.Integer(default=0, description='The amount of upvote - downvote'),
    })

    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('user_id', type=str, required=False, help='Search question by user_id (who created question)')
    get_parser.add_argument('answer_id', type=str, required=False, help='Search all answers by answer_id.')
    get_parser.add_argument('from_date', type=str, required=False, help='Search answers created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search answers created before this data.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
