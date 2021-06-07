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
from app.modules.q_a.answer.improvement.voting.vote_dto import AnswerImprovementVoteDto
from common.controllers.controller import Controller
from common.enum import VotingStatusEnum
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Answer = db.get_model('Answer')
AnswerImprovement = db.get_model('AnswerImprovement')
AnswerImprovementVote = db.get_model('AnswerImprovementVote')


class AnswerImprovementVoteController(Controller):
    query_classname = 'AnswerImprovementVote'
    allowed_ordering_fields = ['created_date', 'updated_date']

    def get_query(self):
        query = self.get_model_class().query
        query = query.join(User, isouter=True).filter(db.or_(AnswerImprovementVote.user == None, User.is_deactivated != True))
        
        return query

    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('from_date'):
            query = query.filter(AnswerImprovementVote.created_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(AnswerImprovementVote.created_date <= dateutil.parser.isoparse(params.get('to_date')))

        return query

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            results = []
            for vote in res.get('data'):
                result = vote._asdict()
                result['user'] = vote.user
                results.append(result)
            res['data'] = marshal(results, AnswerImprovementVoteDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        try:
            improvement = AnswerImprovementVote.query.filter_by(id=object_id).first()
            if improvement is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('AnswerImprovementVote', object_id))
                
            result = improvement._asdict()
            result['user'] = improvement.user
            return send_result(data=marshal(result, AnswerImprovementVoteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, improvement_id, data):
        improvement = AnswerImprovement.query.filter_by(id=improvement_id).first()
        if improvement is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user
        data['user_id'] = current_user.id
        data['improvement_id'] = improvement.id

        try:
            # add or update vote
            is_insert = True
            vote = AnswerImprovementVote.query.filter(AnswerImprovementVote.user_id == data['user_id'], AnswerImprovementVote.improvement_id == data['improvement_id']).first()

            if vote:
                is_insert = False

            vote = self._parse_vote(data=data, vote=vote)
            vote.updated_date = datetime.utcnow()
            if is_insert:
                db.session.add(vote)
            db.session.commit()
            return send_result(data=marshal(vote, AnswerImprovementVoteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def delete(self, improvement_id):
        current_user = g.current_user
        user_id = current_user.id
        try:
            vote = AnswerImprovementVote.query.filter_by(improvement_id=improvement_id, user_id=user_id).first()
            if vote is None:
                return send_error(message='AnswerImprovement vote not found')
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result()
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def update(self):
        pass


    def _parse_vote(self, data, vote=None):
        if vote is None:
            vote = AnswerImprovementVote()

        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'improvement_id' in data:
             try:
                 vote.improvement_id = int(data['improvement_id'])
             except Exception as e:
                 print(e.__str__())
                 pass
                 
        if 'vote_status' in data:
            try:
                vote_status_value = int(data['vote_status'])
                vote.vote_status = VotingStatusEnum(vote_status_value).name
            except Exception as e:
                print(e.__str__())
                pass
        return vote
