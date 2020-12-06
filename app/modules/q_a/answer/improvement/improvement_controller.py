#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# built-in modules
import os
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, g, request, url_for
from flask_restx import marshal
from sqlalchemy import desc
from werkzeug.utils import secure_filename

# own modules
from common.db import db
from app.constants import messages
from app.modules.q_a.answer.improvement.improvement_dto import AnswerImprovementDto
from common.enum import VotingStatusEnum, FileTypeEnum
from common.controllers.controller import Controller
from common.utils.file_handler import append_id, get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import check_sensitive
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
AnswerImprovementVote = db.get_model('AnswerImprovementVote')


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
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Answer', answer_id))
        if not answer.allow_improvement:
            return send_error(message=messages.ERR_ISSUE.format('Answer does not allow improvement'))

        current_user = g.current_user
        data['user_id'] = current_user.id
        data['answer_id'] = answer.id

        try:
            # add new answer
            improvement = self._parse_improvement(data=data, improvement=None)
            is_sensitive = check_sensitive(improvement.content)
            if is_sensitive:
                return send_error(message=messages.ERR_ISSUE.format('Content is not allowed'))
            db.session.add(improvement)
            db.session.commit()
            result = improvement._asdict()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('AnswerImprovement'), data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('AnswerImprovement', e))

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
                if current_user:
                    vote = AnswerImprovementVote.query.filter(AnswerImprovementVote.user_id == current_user.id, AnswerImprovementVote.improvement_id == improvement.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                results.append(result)
            res['data'] = marshal(results, AnswerImprovementDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('AnswerImprovement', e))

    def get_by_id(self, object_id):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('AnswerImprovement', object_id))
                
            result = improvement._asdict()
            result['user'] = improvement.user
            return send_result(data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('AnswerImprovement', e))

    def update(self, object_id, data):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('AnswerImprovement', object_id))

            current_user = g.current_user
            improvement = self._parse_improvement(data=data, improvement=improvement)
            if improvement.content.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer content'))
            is_sensitive = check_sensitive(improvement.content)
            if is_sensitive:
                return send_error(message=messages.ERR_ISSUE.format('Comment content not allowed'))
            if improvement.answer_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer_id'))
            if improvement.user_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
            improvement.updated_date = datetime.utcnow()

            db.session.commit()
            # get user information for each answer.
            result = improvement._asdict()
            result['user'] = improvement.user
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('AnswerImprovement'), data=marshal(result, AnswerImprovementDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format('AnswerImprovement', e))

    def delete(self, object_id):
        try:
            improvement = AnswerImprovement.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('AnswerImprovement', object_id))
            else:
                db.session.delete(improvement)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_DELETE_SUCCESS)

    def _parse_improvement(self, data, improvement=None):
        if improvement is None:
            improvement = AnswerImprovement()
        improvement.answer_id = data.get('answer_id')
        improvement.content = data.get('content')
        improvement.user_id = data.get('user_id')
        return improvement
