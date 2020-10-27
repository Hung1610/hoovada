#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from app import db
from abc import ABC, abstractmethod

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Controller(ABC):
    """
    This class will control all interactions between clients, database server and other things.
    """
    query_classname = ''
    
    def get_model_class(self):
        return db.get_model(self.query_classname)

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Create object and insert to database.
        """
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        """
        Return all objects from database
        """
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        """
        Get object from database by ID
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Updata object from search_data in database
        """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Delete object from database.
        """
        pass
