#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask_restx import marshal

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.question.question import Question
from app.modules.q_a.report.report import Report
from app.modules.q_a.report.report_dto import ReportDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportController(Controller):

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Could not parse params. Check again.')
        user_id, question_id, answer_id, comment_id, from_date, to_date = None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in args:
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in args:
            try:
                comment_id = int(args['comment_id'])
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
        if user_id is None and answer_id is None and comment_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide params to search.')
        query = db.session.query(Report)
        is_filter = False
        if user_id is not None:
            query = query.filter(Report.user_id == user_id)
            is_filter = True
        # if question_id is not None:
        #     query = query.filter(Vote.question_id == question_id)
        #     is_filter = True
        if answer_id is not None:
            query = query.filter(Report.answer_id == answer_id)
            is_filter = True
        if comment_id is not None:
            query = query.filter(Report.comment_id == comment_id)
            is_filter = True
        if from_date is not None:
            query = query.filter(Report.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Report.created_date <= to_date)
            is_filter = True
        if is_filter:
            votes = query.all()
            if votes is not None and len(votes) > 0:
                return send_result(data=marshal(votes, ReportDto.model_response), message='Success')
            else:
                return send_result(message='Could not find any votes.')
        else:
            return send_error(message='Could not find votes. Please check your parameters again.')

    def create_report_user(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form.')
        if not 'user_id' in data:
            return send_error(message='The user_id must be included.')
        if not 'reported_user_id' in data:
            return send_error(message='Please fill question_id')
        try:
            report = self._parse_report(data=data, report=None)
            if report.question_id and report.answer_id and report.comment_id:
                return send_result('Stop hacking our system.')
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            # update other values
            try:
                user = User.query.filter_by(id=report.user_id).first()
                # user_reported = User.query.filter_by(id=user_id).first()
            except Exception as e:
                print(e.__str__())
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create report record.')

    def create_report_question(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form.')
        if not 'user_id' in data:
            return send_error(message='The user_id must be included.')
        if not 'question_id' in data:
            return send_error(message='Please fill question_id')
        try:
            report = self._parse_report(data=data, report=None)
            if report.question_id and report.answer_id and report.comment_id:
                return send_result('Stop hacking our system.')
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            # update other values
            try:
                user = User.query.filter_by(id=report.user_id).first()
                question = Question.query.filter_by(id=report.question_id).first()
                user_reported = User.query.filter_by(id=question.user_id).first()
                user.question_report_count += 1
                user_reported.question_reported_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create report record.')

    def create_report_answer(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form.')
        if not 'user_id' in data:
            return send_error(message='The user_id must be included.')
        if not 'answer_id' in data:
            return send_error(message='Please fill answer_id')
        try:
            report = self._parse_report(data=data, report=None)
            if report.question_id and report.answer_id and report.comment_id:
                return send_result('Stop hacking our system.')
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            # update other values
            try:
                user = User.query.filter_by(id=report.user_id).first()
                answer = Answer.query.filter_by(id=report.answer_id).first()
                user_reported = User.query.filter_by(id=answer.user_id).first()
                user.answer_report_count += 1
                user_reported.answer_reported_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create report record.')

    def create_report_comment(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form.')
        if not 'user_id' in data:
            return send_error(message='The user_id must be included.')
        if not 'comment_id' in data:
            return send_error(message='Please fill comment_id')
        try:
            report = self._parse_report(data=data, report=None)
            if report.question_id and report.answer_id and report.comment_id:
                return send_result('Stop hacking our system.')
            report.created_date = datetime.utcnow()
            db.session.add(report)
            db.session.commit()
            # update other values
            try:
                user = User.query.filter_by(id=report.user_id).first()
                comment = Comment.query.filter_by(id=report.comment_id).first()
                user_reported = User.query.filter_by(id=comment.user_id).first()
                user.comment_report_count += 1
                user_reported.comment_reported_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
            return send_result(data=marshal(report, ReportDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create report record.')

    def create(self, data):
        pass

    def get(self):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_report(self, data, report=None):
        '''
        Parse dictionary form data to report.
        ----------------------

        :param data: A dictionary form data.

        :param report: A report as a param.

        :return: A report.
        '''
        if report is None:
            report = Report()
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
        if 'answer_id' in data:
            try:
                report.answer_id = int(data['answer_id'])
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
