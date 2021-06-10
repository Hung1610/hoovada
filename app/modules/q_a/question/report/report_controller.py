#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.q_a.question.report.report_dto import QuestionReportDto
from common.controllers.controller import Controller
from common.enum import ReportTypeEnum
from common.models import QuestionReport
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportController(Controller):

    def get(self, question_id, args):
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
        
        try:
            query = QuestionReport.query
            if user_id is not None:
                query = query.filter(QuestionReport.user_id == user_id)
            
            if question_id is not None:
                query = query.filter(QuestionReport.question_id == question_id)
            
            if from_date is not None:
                query = query.filter(QuestionReport.created_date >= from_date)
            
            if to_date is not None:
                query = query.filter(QuestionReport.created_date <= to_date)
            
            reports = query.all()        
            return send_result(data=marshal(reports, QuestionReportDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def create(self, question_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['question_id'] = question_id

        if 'report_type' in data and data['report_type'] == 'DUPLICATE' and 'duplicated_question_id' not in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('duplicated_question_id'))
        
        try:
            report = self._parse_report(data=data, report=None)
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            return send_result()
            
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):

        try:
            query = QuestionReport.query
            report = query.filter(QuestionReport.id == object_id).first()
            if report is None:
                return send_error(message=messages.ERR_NOT_FOUND)
                
            return send_result(data=marshal(report, QuestionReportDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def update(self):
        pass


    def delete(self):
        pass


    def _parse_report(self, data, report=None):

        if report is None:
            report = QuestionReport()

        if 'user_id' in data:
            try:
                report.user_id = int(data['user_id'])
            except Exception as e:
                pass

        if 'question_id' in data:
            try:
                report.question_id = int(data['question_id'])
            except Exception as e:
                pass
                
        if 'duplicated_question_id' in data:
            try:
                report.question_id = int(data['duplicated_question_id'])
            except Exception as e:
                pass

        if 'description' in data:
            try:
                report.description = data['description']
            except Exception as e:
                pass
        
        if 'report_type' in data:
            try:
                report_type = int(data['report_type'])
                report.report_type = ReportTypeEnum(report_type).name
            except Exception as e:
                print(e.__str__())
                pass

        return report
