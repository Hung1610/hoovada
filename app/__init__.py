#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource
from flask_restx import Namespace

# own modules
from app.app import init_app, db, cache
from app.apis import init_api
from app.utils.response import send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


ns_health = Namespace(name='health')


@ns_health.route('/')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes
        
        Args:
            None

        Returns
           None - 200 code for success 
        """
        
        return send_result(message="OK!", code=200)


def create_app(mode):
    """ Create an app

    Args:
        mode (string): mode that the app is running on

    Returns:
        object - An initialized app
    """

    app = init_app(mode)
    api = init_api(mode)
    api.init_app(app)
    api.add_namespace(ns_health)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    
    return app
