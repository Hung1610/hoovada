#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app_socketio.modules.chat.chat_namespace import ChatNamespace
from app_socketio.app import socketio


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

socketio.on_namespace(ChatNamespace('/chat'))