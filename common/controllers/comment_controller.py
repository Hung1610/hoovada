#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseCommentController(Controller):
    related_field_name = None

    def _parse_comment(self, data, comment=None):
        if comment is None:
            comment = self.get_model_class()()

        if 'comment' in data:
            comment.comment = data['comment']
        
        if self.related_field_name in data:
            try:
                setattr(comment, self.related_field_name, int(data[self.related_field_name]))
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'user_id' in data:
            try:
                comment.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if g.current_user_is_admin:
            if 'allow_favorite' in data:
                try:
                    comment.allow_favorite = bool(data['allow_favorite'])
                except Exception as e:
                    print(e.__str__())
                    pass
        if 'entity_type' in data:
            try:
                comment.entity_type = data['entity_type']
            except Exception as e:
                print(e.__str__())
                pass

        if 'organization_id' in data:
            try:
                comment.organization_id = int(data['organization_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return comment
