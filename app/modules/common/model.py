#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC, abstractmethod
from app.app import db

# third-party modules
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import inspect

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Model(db.Model):
    """
    Class entity is parent class for all other class
    """
    __abstract__ = True

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
