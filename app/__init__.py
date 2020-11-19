#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules

# own modules
from app.app import init_app, dramatiq
from app.apis import init_api

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def create_app():
    """ Create an app

    Returns:
        object - An initialized app
    """

    app = init_app()
    api = init_api()
    api.init_app(app)
    
    return app

flask_app = create_app()
broker = dramatiq.broker
