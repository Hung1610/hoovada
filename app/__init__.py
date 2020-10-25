#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules

# own modules
from app.app import init_app, db, cache
from app.apis import init_api

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


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
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    
    return app
