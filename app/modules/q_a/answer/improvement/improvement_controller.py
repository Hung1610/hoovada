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
from app.modules.q_a.answer.improvement.improvement_dto import AnswerImprovementDto
from common.enum import VotingStatusEnum, FileTypeEnum
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result
from common.utils.types import UserRole
from common.utils.util import encode_file_name
from common.utils.wasabi import upload_file

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Answer = db.get_model('Answer')
AnswerImprovement = db.get_model('AnswerImprovement')


class AnswerImprovementController(Controller):
    query_classname = 'AnswerImprovement'
    allowed_ordering_fields = ['created_date', 'updated_date']

    def create(self, data, answer_id):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'content' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('content'))

        answer = Answer.query.filter_by(id=answer_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        if not answer.allow_improvement:
            return send_error(message=messages.ERR_ISSUE.format('Answer does not allow improvement'))

        current_user = g.current_user
        data['user_id'] = current_user.id
        data['answer_id'] = answer.id

        try:
            # add new answer
            improvement = self._parse_improvement(data=data, improvement=None)

            db.session.add(improvement)
            db.session.commit()
            result = improvement._asdict()
            return send_result( data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            current_user = g.current_user
            # get user information for each improvement.
            results = []
            for improvement in res.get('data'):
                result = improvement._asdict()
                result['user'] = improvement.user
                results.append(result)
            res['data'] = marshal(results, AnswerImprovementDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND)
                
            result = improvement._asdict()
            result['user'] = improvement.user
            return send_result(data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            improvement = self._parse_improvement(data=data, improvement=improvement)
            if improvement.content.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer content'))

            if improvement.answer_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer_id'))
            if improvement.user_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
            improvement.updated_date = datetime.utcnow()

            db.session.commit()
            # get user information for each answer.
            result = improvement._asdict()
            result['user'] = improvement.user
            return send_result(data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            else:
                db.session.delete(improvement)
                db.session.commit()
                return send_result()
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_query(self):
        query = self.get_model_class().query
        query = query.join(User, isouter=True).filter(db.or_(AnswerImprovement.user == None, User.is_deactivated != True))
        return query


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(AnswerImprovement.created_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(AnswerImprovement.created_date <= dateutil.parser.isoparse(params.get('to_date')))

        return query


    def _parse_improvement(self, data, improvement=None):
        if improvement is None:
            improvement = AnswerImprovement()
        improvement.answer_id = data.get('answer_id')
        improvement.content = data.get('content')
        improvement.user_id = data.get('user_id')
        return improvement
