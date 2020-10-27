#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request, current_app
from flask_restx import marshal

# own modules
from app import db
from app.constants import messages
from common.controllers.controller import Controller
from app.modules.post.post import Post
from app.modules.post.report.report import PostReport
from app.modules.post.report.report_dto import ReportDto
from app.modules.user.user import User
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType
from common.utils.permission import has_permission

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportController(Controller):
    def get(self, post_id, args):
        user_id, from_date, to_date = None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'from_date' in args:
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
            
        query = PostReport.query
        if user_id is not None:
            query = query.filter(PostReport.user_id == user_id)
        if post_id is not None:
            query = query.filter(PostReport.post_id == post_id)
        if from_date is not None:
            query = query.filter(PostReport.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PostReport.created_date <= to_date)
        reports = query.all()
        return send_result(data=marshal(reports, ReportDto.model_response), message='Success')

    def create(self, post_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        current_user, _ = current_app.get_logged_user(request)
        if not has_permission(current_user.id, PermissionType.REPORT):
            return send_error(code=401, message='You have no authority to perform this action')
        data['user_id'] = current_user.id
        data['post_id'] = post_id
        try:
            report = self._parse_report(data=data, report=None)
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Post Report'))

    def get_by_id(self, object_id):
        query = PostReport.query
        report = query.filter(PostReport.id == object_id).first()
        if report is None:
            return send_error(message=messages.ERR_NOT_FOUND.format('Post Report'))
        else:
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_report(self, data, report=None):
        """ Parse dictionary form data to report.
        
        Args:
            data: A dictionary form data.
            report: A report as a param.

        Returns: 
            A report.
        """

        if report is None:
            report = PostReport()
        if 'user_id' in data:
            try:
                report.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'post_id' in data:
            try:
                report.post_id = int(data['post_id'])
            except Exception as e:
                pass
        if 'inappropriate' in data:
            try:
                report.inappropriate = bool(data['inappropriate'])
            except Exception as e:
                pass
        if 'description' in data:
            report.description = data['description']

        return report
