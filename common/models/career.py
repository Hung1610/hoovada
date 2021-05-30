#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

# built-in modules
from slugify import slugify

# third-party modules
from sqlalchemy import event

# own modules
from common.db import db
from common.models.mixins import AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Career(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'career'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    slug = db.Column(db.String(255), index=True)
    description = db.Column(db.UnicodeText)
    requirements = db.Column(db.UnicodeText)
    location = db.Column(db.UnicodeText)
    contact = db.Column(db.UnicodeText)
    salary_from = db.Column(db.Integer, server_default="0")
    salary_to = db.Column(db.Integer, server_default="0")
    expire_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,\
        db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User',\
        lazy=True)  # one-to-many relationship with table User

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

event.listen(Career.title, 'set', Career.generate_slug, retval=False)
