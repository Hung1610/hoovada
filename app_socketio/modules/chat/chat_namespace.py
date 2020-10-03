#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_socketio import Namespace, send, emit, join_room, leave_room

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class ChatNamespace(Namespace):

    def on_connect(self):
        print('Someone connected.')

    def on_disconnect(self):
        print('Someone disconnected.')

    def on_message(self, data):
        username = data['username']
        room = data['room']
        message = data['message']
        send('{}: {}'.format(username, message), room=room)

    def on_join(self, data):
        username = data['username']
        room = data['room']
        join_room(room)
        send(username + ' has entered the room.', room=room)

    def on_leave(self, data):
        username = data['username']
        room = data['room']
        leave_room(room)
        send(username + ' has left the room.', room=room)
