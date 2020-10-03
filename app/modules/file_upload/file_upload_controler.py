#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import request
from flask_restx import marshal

# own modules
from app.modules.auth.auth_controller import AuthController
from app.modules.common.controller import Controller
from app.modules.file_upload.file_upload_dto import FileUploadDto
from app.utils.file_handler import get_file_name_extension
from app.utils.response import send_error, send_result
from app.utils.util import encode_file_name
from app.utils.wasabi import upload_file

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class FileUploadController(Controller):

    def create(self, data):
        pass

    def get(self):
        pass

    def get_by_id(self, object_id):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def upload_image(self, args):
        if not isinstance(args, dict) or not 'image' in args:
            return send_error(message='Your request does not contain image.')
        # upload here
        user, message = AuthController.get_logged_user(request)
        # user = User.query.filter_by(id=id).first()
        if user is None:
            return send_error(message)
        photo = args['image']
        if photo:
            filename = photo.filename
            file_name, ext = get_file_name_extension(filename)
            # file_name = 'user_' + str(user.id) + '_avatar'
            file_name = encode_file_name(file_name) + ".png"
            user_id = user.id
            bucket = 'hoovada'
            sub_folder = encode_file_name(str(user_id))
            try:
                url = upload_file(file=photo, file_name=file_name, sub_folder=sub_folder)
                result = dict()
                result['url'] = url
                return send_result(data=marshal(result, FileUploadDto.model), message='Upload image successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your avatar.')
        else:
            return send_error(message='Please attach or check your photo before uploading.')
