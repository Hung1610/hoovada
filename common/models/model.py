#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC, abstractmethod
from common.utils.util import get_model, get_model_by_tablename
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import inspect
# third-party modules
from sqlalchemy.ext.declarative import as_declarative

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


SQLAlchemy.get_model = get_model
SQLAlchemy.get_model_by_tablename = get_model_by_tablename
db = SQLAlchemy()


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