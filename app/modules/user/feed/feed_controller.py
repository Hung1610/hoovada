#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
import json
from http import HTTPStatus

# third-party modules
import requests
from flask import g
from flask_restx import marshal

# own modules
from app.constants import messages
from app.settings.config import BaseConfig
from common.db import db
from app.modules.user.feed.feed_dto import UserFeedDto
from common.controllers.controller import Controller
from common.utils.response import send_paginated_result, send_error


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."



class UserFeedController(Controller):

    def get(self, args):

        if g.current_user is None:
            return send_error(message=messages.ERR_NOT_LOGIN)
        
        try:
            get_data = args.get('get_data', False)
            api_endpoint = '/api/feed' if get_data is False else '/api/feed_all_data'

            get_feed_url = '{}{}'.format(BaseConfig.FEED_SERVICE_URL, api_endpoint)

            params={'user_id': g.current_user.id}
            
            page = 1
            if 'page' in args:
                page = args.get('page', 1)
                params['page'] = page

            if 'per_page' in args:
                params['per_page'] = args['per_page']
            
            response = requests.get(url=get_feed_url, params=params)
            resp = json.loads(response.content)
            if response.status_code == HTTPStatus.OK:
                if get_data is False:
                    data = marshal(resp['data'], UserFeedDto.model_feed_details_response)
                else:
                    data = marshal(resp['data'], UserFeedDto.model_feed_all_data_details_response)
                return send_paginated_result(data=data, page=page, total=len(data), message='Success')
            
            else:
                return send_error(message=messages.ERR_ISSUE.format(resp.get('message')))   
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('user feed', str(e)))

    def get_by_id(self):
        return

    def delete(self):
        return

    def create(self):
        return

    def update(self):
        return