#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal

# own modules
from app import db
from app.common.controller import Controller
from app.modules.q_a.answer.comment.comment import AnswerComment
from app.modules.q_a.answer.comment.report.report import AnswerCommentReport
from app.modules.q_a.answer.comment.report.report_dto import AnswerCommentReportDto
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportController(Controller):
    def get(self, comment_id, args):
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
            
        query = AnswerCommentReport.query
        if user_id is not None:
            query = query.filter(AnswerCommentReport.user_id == user_id)
        if comment_id is not None:
            query = query.filter(AnswerCommentReport.comment_id == comment_id)
        if from_date is not None:
            query = query.filter(AnswerCommentReport.created_date >= from_date)
        if to_date is not None:
            query = query.filter(AnswerCommentReport.created_date <= to_date)
        reports = query.all()
        if reports is not None and len(reports) > 0:
            return send_result(data=marshal(reports, AnswerCommentReportDto.model_response), message='Success')
        else:
            return send_result(message='Report not found')

    def create(self, comment_id, data):
        if not isinstance(data, dict):
            return send_error(message='Data is wrong format')
        
        current_user, _ = AuthController.get_logged_user(request)
        data['user_id'] = current_user.id
        data['comment_id'] = comment_id
        try:
            report = self._parse_report(data=data, report=None)
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            return send_result(data=marshal(report, AnswerCommentReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to create comment report')

    def get_by_id(self, object_id):
        query = AnswerCommentReport.query
        report = query.filter(AnswerCommentReport.id == object_id).first()
        if report is None:
            return send_error(message='Report not found')
        else:
            return send_result(data=marshal(report, AnswerCommentReportDto.model_response), message='Success')

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
            report = AnswerCommentReport()
        if 'user_id' in data:
            try:
                report.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'comment_id' in data:
            try:
                report.comment_id = int(data['comment_id'])
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
