#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from common.dramatiq_producers import update_reputation
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.poll.voting.vote_dto import PollVoteDto
from common.enum import VotingStatusEnum
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Reputation = db.get_model('Reputation')
PollVote = db.get_model('PollVote')


class PollVoteController(Controller):
    def get(self, args, poll_id = None):

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
        if user_id is None and poll_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide query parameters.')

        query = PollVote.query
        if user_id is not None:
            query = query.filter(PollVote.user_id == user_id)
        if poll_id is not None:
            query = query.filter(PollVote.poll_id == poll_id)
        if from_date is not None:
            query = query.filter(PollVote.created_date >= from_date)
        if to_date is not None:
            query = query.filter(PollVote.created_date <= to_date)
        votes = query.all()
        if votes is not None and len(votes) > 0:
            return send_result(data=marshal(votes, PollVoteDto.model_response), message='Success')
        else:
            return send_result(message='Poll vote not found')

    def get_by_id(self, object_id):
        if id is None:
            return send_error(message='Please provide id')
        vote = PollVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message='Poll vote not found')
        else:
            return send_result(data=marshal(vote, PollVoteDto.model_response), message='Success')

    def create(self, poll_id, data):
        current_user, _ = current_app.get_logged_user(request)
        if not isinstance(data, dict):
            return send_error(message='Wrong data format')
        data['user_id'] = current_user.id
        data['poll_id'] = poll_id
        
        try:
            # add or update vote
            is_insert = True
            vote = PollVote.query.filter(PollVote.user_id == data['user_id'], \
                PollVote.poll_id == data['poll_id']).first()
        
            if vote:
                is_insert = False
            vote = self._parse_vote(data=data, vote=vote)
            vote.updated_date = datetime.utcnow()
        
            if is_insert:
                db.session.add(vote)
            db.session.commit()
            return send_result(data=marshal(vote, PollVoteDto.model_response), message='Success')
        
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message='Failed to create poll vote.')

    def delete(self, poll_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            vote = PollVote.query.filter_by(poll_id=poll_id, user_id=user_id).first()
            if vote is None:
                return send_error(message='Poll vote not found')
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Poll vote deleted successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete poll vote')

    def update(self, object_id, data):
        """ Update object from search_data in database
        
        Args:
            object_id:
            data:
        
        Returns:
        """
        pass

    def _parse_vote(self, data, vote=None):
        if vote is None:
            vote = PollVote()
        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'poll_id' in data:
             try:
                 vote.poll_id = int(data['poll_id'])
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
