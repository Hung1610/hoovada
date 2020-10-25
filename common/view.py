#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC, abstractmethod

# third-party modules
from flask_restx import Resource as BaseResource

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Resource(BaseResource):
    """
    Abstract class from which all view classes will inherit.
    """

    # @abstractmethod
    # def get(self):
    #     pass
    #
    # @abstractmethod
    # def post(self):
    #     pass
    pass


class ResourceId(BaseResource):
    # @abstractmethod
    # def get(self, object_id):
    #     pass
    #
    # @abstractmethod
    # def put(self, object_id, data):
    #     pass
    #
    # @abstractmethod
    # def delete(self, object_id):
    #     pass
    pass
