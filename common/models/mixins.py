#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from sqlalchemy.sql import expression

# own modules
from app.app import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AuditCreateMixin(object):
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class AuditUpdateMixin(object):
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)

class AnonymousMixin(object):
    is_anonymous = db.Column(db.Boolean, server_default=expression.false())

    @property
    def display_user_id(self):
        if self.is_anonymous:
            return self.user_id if g.current_user.id == self.user_id else None
        return self.user_id

    @property
    def display_user(self):
        if self.is_anonymous:
            return self.user if g.current_user.id == self.user_id else None
        return self.user
    