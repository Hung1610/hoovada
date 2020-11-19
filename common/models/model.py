#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC, abstractmethod

from sqlalchemy import inspect
# third-party modules
from sqlalchemy.ext.declarative import as_declarative

from app.app import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return None

class Model(db.Model):
    """
    Class entity is parent class for all other class
    """
    __abstract__ = True

    def _asdict(self):
        # return {c.key: getattr(self, c.key)
        #         for c in inspect(self).mapper.column_attrs}
        object_dict = {attr: catch(getattr, self, attr) for attr in dir(self) if not attr.startswith("__")}
        return object_dict