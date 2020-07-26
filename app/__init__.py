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


ns_hello = Namespace(name='hello')
api = init_api()


@ns_hello.route('')
class HelloHoovada(Resource):
    def get(self):
        """
        Testing the API

        :return the 'Hello Hoovada' text
        """
        return send_result(message="Hello Hoovada")


def init_hello():
    '''
    This is testing
    '''


def create_app(config):
    """
    Create an app

    :param: config

    :return: an initialized app
    """
    init_hello()
    app = init_app(config_name=config)
    api.init_app(app)
    api.add_namespace(ns_hello)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    return app
