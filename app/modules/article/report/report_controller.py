#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from app.modules.article.report.report_dto import ReportDto
from common.controllers.controller import Controller
from common.enum import ReportTypeEnum
from common.models import Article, ArticleReport, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportController(Controller):
    def get(self, article_id, args):
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
            query = ArticleReport.query
            if user_id is not None:
                data_role = self.get_role_data()
                if data_role['role'] == 'user':
                    query = query.filter(ArticleReport.user_id == user_id, ArticleReport.entity_type == data_role['role'])
                if data_role['role'] == 'organization':
                    query = query.filter(ArticleReport.organization_id == data_role['organization_id'], ArticleReport.entity_type == data_role['role'])
            if article_id is not None:
                query = query.filter(ArticleReport.article_id == article_id)
            if from_date is not None:
                query = query.filter(ArticleReport.created_date >= from_date)
            if to_date is not None:
                query = query.filter(ArticleReport.created_date <= to_date)
            reports = query.all()
            return send_result(data=marshal(reports, ReportDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        data = self.add_org_data(data)      
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['article_id'] = article_id
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
            query = ArticleReport.query
            report = query.filter(ArticleReport.id == object_id).first()
            
            if report is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            return send_result(data=marshal(report, ReportDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self):
        pass


    def delete(self, object_id):
        pass


    def _parse_report(self, data, report=None):
        """ Parse dictionary form data to report"""

        if report is None:
            report = ArticleReport()

        if 'user_id' in data:
            try:
                report.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'article_id' in data:
            try:
                report.article_id = int(data['article_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'description' in data:
            try:
                report.description = data['description']
            except Exception as e:
                print(e.__str__())
                pass

        if 'report_type' in data:
            try:
                report_type = int(data['report_type'])
                report.report_type = ReportTypeEnum(report_type).name
            except Exception as e:
                print(e.__str__())
                pass
        if 'entity_type' in data:
            try:
                report.entity_type = data['entity_type']
            except Exception as e:
                print(e.__str__())
                pass

        if 'organization_id' in data:
            try:
                report.organization_id = int(data['organization_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return report
