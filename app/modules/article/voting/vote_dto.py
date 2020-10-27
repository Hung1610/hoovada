#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace, reqparse

# own modules
from common.models.vote import VotingStatusEnum
from common.dto import Dto


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class VoteDto(Dto):
    name = 'article_vote'
    api = Namespace(name, description="Article voting operations")

    model_request_article = api.model('vote_request_article_vote', {
        'vote_status': fields.Integer(description='1 - Neutral, 2 - Upvote, 3 - Downvote', default=False)
    })

    model_response = api.model('vote_response_article_vote', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the vote record in database'),
        'user_id': fields.Integer(description='The user ID'),
        'article_id': fields.Integer(description='The ID of the article'), 
        'vote_status': fields.String(description='The voting status', attribute='vote_status.name'),
        'created_date': fields.DateTime(description='The date user voted'),
        'updated_date': fields.DateTime(description='The date user modified vote value')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search votes by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all votes by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all votes by finish voting date.')