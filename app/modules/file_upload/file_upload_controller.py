#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from app.modules.file_upload.file_upload_dto import FileUploadDto
from app.constants import messages
from common.controllers.controller import Controller
from common.utils.file_handler import get_file_name_extension
from common.utils.response import send_error, send_result
from common.utils.util import encode_file_name
from common.utils.wasabi import upload_file

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class FileUploadController(Controller):

    def create(self, data):
        current_user = g.current_user

        file = data.get('file')

        if not file:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))
        
        try:
            filename = file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            sub_folder = '{}/{}'.format('file', current_user.id if current_user else 'guest')
            url = upload_file(file=file, file_name=file_name, sub_folder=sub_folder)
            result = {'url': url}
            return send_result(data=marshal(result, FileUploadDto.model))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def get(self):
        pass

    def get_by_id(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
