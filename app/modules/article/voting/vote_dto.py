#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class VoteDto(Dto):
    name = 'vote'
    api = Namespace(name)
    model_request_question = api.model('vote_request_question', {
        'user_id': fields.Integer(description='The user ID'),
        'question_id': fields.Integer(description='The ID of the question to vote'),
        'up_vote': fields.Boolean(description='Set to `true` if upvote', default=False),
        'down_vote': fields.Boolean(description='Set to `True` if downvote', default=False)
    })

    model_request_answer = api.model('vote_request_answer', {
        'user_id': fields.Integer(description='The user ID'),
        'answer_id': fields.Integer(description='The ID of the answer to vote'),
        'up_vote': fields.Boolean(description='Set to `true` if upvote', default=False),
        'down_vote': fields.Boolean(description='Set to `True` if downvote', default=False)
    })

    model_request_comment = api.model('vote_request_comment', {
        'user_id': fields.Integer(description='The user ID'),
        'comment_id': fields.Integer(description='The ID of the comment to vote'),
        'up_vote': fields.Boolean(description='Set to `true` if upvote', default=False),
        'down_vote': fields.Boolean(description='Set to `True` if downvote', default=False)
    })

    model_response = api.model('vote_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the vote record in database'),
        'user_id': fields.Integer(description='The user ID'),
        'question_id': fields.Integer(description='The ID of the question'),  # chua vote cho question
        'answer_id': fields.Integer(description='The ID of the answer'),
        'comment_id': fields.Integer(description='The ID of the comment'),
        'up_vote': fields.Boolean(description='The value of upvote'),
        'down_vote': fields.Boolean(description='The value of downvote'),
        'created_date': fields.DateTime(description='The date user voted'),
        'updated_date': fields.DateTime(description='The date user modified vote value')
    })
