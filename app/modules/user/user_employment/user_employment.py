#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from common.db import db
# own modules
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class UserEmployment(Model):
    __tablename__ = 'user_employment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    position = db.Column(db.String(255))
    company = db.Column(db.String(255))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    is_current = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
