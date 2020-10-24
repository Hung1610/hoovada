#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC, abstractmethod

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Controller(ABC):
    """
    This class will control all interactions between clients, database server and other things.
    """

    @abstractmethod
    def create(self, data):
        """
        Create object and insert to database.
        :param data:
        :return:
        """
        pass

    @abstractmethod
    def get(self):
        """
        Return all objects from database
        :return:
        """
        pass

    @abstractmethod
    def get_by_id(self, object_id):
        """
        Get object from database by ID
        :param object_id:
        :return:
        """
        pass

    @abstractmethod
    def update(self, object_id, data):
        """
        Updata object from search_data in database
        :param object_id:
        :param data:
        :return:
        """
        pass

    @abstractmethod
    def delete(self, object_id):
        """
        Delete object from database.
        :param object_id:
        :return:
        """
        pass
