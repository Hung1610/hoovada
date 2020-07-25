#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields
from flask_restx_patched import Namespace

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class TimelineDto(Dto):
    name = 'timeline'
    api = Namespace(name)
    model = api.model(name, {

    })