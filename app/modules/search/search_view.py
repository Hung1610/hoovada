#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.search.search_controller import SearchController
# own modules
from app.modules.search.search_dto import SearchDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = SearchDto.api
search_response = SearchDto.search_response

parser = reqparse.RequestParser()
parser.add_argument('value', type=str, required=True, help='The value of the search')


@api.route('/event_search')
@api.expect(parser)
class Search(Resource):
    @api.response(code=200, model=search_response, description='Model for success response.')
    def get(self):
        """ 
        Get search results satisfy conditions.
        """

        args = parser.parse_args()
        controller = SearchController()
        return controller.search(args=args)