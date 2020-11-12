#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import Flask
from flask_socketio import SocketIO

# own modules
from app_socketio.modules.chat.chat_namespace import ChatNamespace
from app_socketio.settings.config import config_by_name

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

socketio = SocketIO()

def init_app(config_name):
    app = Flask(__name__, static_folder='static')
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_by_name[config_name])

    socketio.init_app(app, cors_allowed_origins="*")
    socketio.on_namespace(ChatNamespace('/chat'))

    return app
