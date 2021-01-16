#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_sqlalchemy import BaseQuery
from sqlalchemy.sql import expression

# own modules
from common.db import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None

class AuditCreateMixin(object):
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class AuditUpdateMixin(object):
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
                              
class SoftDeleteMixin(object):
    query_class = QueryWithSoftDelete
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())

class AnonymousMixin(object):
    is_anonymous = db.Column(db.Boolean, nullable=False, server_default=expression.false())

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
    