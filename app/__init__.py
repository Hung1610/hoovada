#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource
from flask_restx import Namespace

# own modules
from .app import init_app, db
from .apis import init_api
from app.utils.response import send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


ns_hello = Namespace(name='health')
api = init_api()


@ns_hello.route('/health')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes
        
        Args:
            None

        Returns
           200 code for success 
        """
        return send_result(message="OK!", code=200)


def create_app(config):
    """ Create an app

    Args:
        config (dict)

    Returns:
        object - An initialized app
    """

    app = init_app(config_name=config)
    api.init_app(app)
    api.add_namespace(ns_hello)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    return app
