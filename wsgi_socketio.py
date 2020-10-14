#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app_socketio import create_app

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

socketio_app = create_app('prod')

if __name__ == "__main__":
    socketio.run(socketio_app)