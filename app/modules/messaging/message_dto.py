#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields

# own modules
from app.common.dto import Dto
from flask_restx_patched import Namespace

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class MessageDto(Dto):
    name = 'message'
    api = Namespace(name, description="Message operations")
    model = api.model(name, {
        'id': fields.Integer(required=False),
        'message': fields.DateTime(),
        'sent_time': fields.DateTime(),
        'read_time': fields.DateTime(),
        'sender_id': fields.Integer(),
        'recipient_id': fields.Integer()
    })
