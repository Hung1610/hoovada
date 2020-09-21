#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import reqparse

# built-in modules
from abc import ABC, abstractmethod

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Dto(ABC):

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def api(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError()

    paginated_request_parser = reqparse.RequestParser()
    paginated_request_parser.add_argument('page', type=int, required=True, help='Page no of results.')
    paginated_request_parser.add_argument('per_page', type=int, required=True, help='Number of result per page.')
