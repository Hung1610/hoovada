#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

# own modules
from app.modules.file_upload.file_upload_controller import FileUploadController
from app.modules.file_upload.file_upload_dto import FileUploadDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = FileUploadDto.api

upload = api.parser()
upload.add_argument('file', location='files',
                           type=FileStorage, required=True, help='The file to upload')


@api.route('')
class UploadFile(Resource):
    @api.expect(upload)
    def post(self):
        """Upload file"""
        
        args = upload.parse_args()
        controller = FileUploadController()
        return controller.create(data=args)