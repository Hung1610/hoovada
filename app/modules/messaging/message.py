#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Message(Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.UnicodeText)
    sent_time = db.Column(db.DateTime)
    read_time = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer)
    recipient_id = db.Column(db.Integer)
