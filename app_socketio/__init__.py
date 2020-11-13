#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app_socketio.app import init_app, socketio

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def create_app():
    """ Create an app

    Args:
        mode (string): mode that the app is running on

    Returns:
        object - An initialized app
    """

    app = init_app()
    
    return app
