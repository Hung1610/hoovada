#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
