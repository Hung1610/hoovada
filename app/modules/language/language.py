#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules

# own modules
from app import db
from app.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Language(Model):
    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
