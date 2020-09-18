#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserLocation(Model):
    __tablename__ = 'user_location'

    id = db.Column(db.Integer, primary_key=True)
    location_detail = db.Column(db.UnicodeText)
    is_current = db.Column(db.Boolean, default=False)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

