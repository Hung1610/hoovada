#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from common.dramatiq_producers import update_reputation
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.q_a.answer.voting.vote_dto import AnswerVoteDto
from common.enum import VotingStatusEnum
from common.controllers.controller import Controller
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType, UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Reputation = db.get_model('Reputation')
AnswerVote = db.get_model('AnswerVote')


class AnswerVoteController(Controller):

    def create(self, answer_id, data):
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        current_user = g.current_user

        if not (UserRole.is_admin(current_user.admin) or has_permission(current_user.id, PermissionType.ANSWER_VOTE)):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            is_insert = True
            vote = AnswerVote.query.filter(AnswerVote.user_id == data['user_id'], AnswerVote.answer_id == data['answer_id']).first()

            if vote:
                is_insert = False
            vote = self._parse_vote(data=data, vote=vote)
            vote.updated_date = datetime.utcnow()
            if is_insert:
                db.session.add(vote)

            db.session.commit()
            answer = vote.answer
            user_voted = answer.user
            for topic in answer.question.topics:
                update_reputation.send(topic.id, user_voted.id)
                update_reputation.send(topic.id, current_user.id, is_voter=True)
            return send_result(data=marshal(vote, AnswerVoteDto.model_response), message=messages.MSG_CREATE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args, answer_id=None):

        answer_id, user_id, from_date, to_date = None, None, None, None
        if 'user_id' in args:
            try:
                vote.user_id = int(args['user_id'])
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
            query = AnswerVote.query
            if user_id is not None:
                query = query.filter(AnswerVote.user_id == user_id)
            if answer_id is not None:
                query = query.filter(AnswerVote.answer_id == answer_id)
            if from_date is not None:
                query = query.filter(AnswerVote.created_date >= from_date)
            if to_date is not None:
                query = query.filter(AnswerVote.created_date <= to_date)
            votes = query.all()
            if votes is not None and len(votes) > 0:
                return send_result(data=marshal(votes, AnswerVoteDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        vote = AnswerVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message=messages.MSG_GET_SUCCESS)
        else:
            return send_result(data=marshal(vote, AnswerVoteDto.model_response), message=messages.MSG_GET_SUCCESS)


    def delete(self, answer_id):
        if answer_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        current_user = g.current_user
        user_id = current_user.id
        try:
            vote = AnswerVote.query.filter_by(answer_id=answer_id, user_id=user_id).first()
            if vote is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            db.session.delete(vote)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def update(self):
        pass


    def _parse_vote(self, data, vote=None):
        if vote is None:
            vote = AnswerVote()

        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'answer_id' in data:
             try:
                 vote.answer_id = int(data['answer_id'])
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
