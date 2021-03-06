#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum
from datetime import datetime

# own modules
from common.db import db
from common.enum import BanTypeEnum
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserBan(Model):
    __tablename__ = 'user_ban'

    id = db.Column(db.Integer, primary_key=True)
    ban_by = db.Column(db.String(255))
    ban_type = db.Column(db.Enum(BanTypeEnum, validate_strings=True), nullable=False, server_default="EMAIL")
    expiry_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
