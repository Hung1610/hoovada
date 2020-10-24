#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class FileUploadDto(Dto):
    name = 'file_upload'
    api = Namespace(name=name, description="Uploading operations")
    model = api.model(name, {
        'url': fields.String(required=True, description = 'The url to file store in server.')
    })
