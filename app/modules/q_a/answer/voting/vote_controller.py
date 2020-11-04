#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import current_app, request
from flask_restx import marshal

# own modules
from app.app import db
from app.constants import messages
from app.modules.q_a.answer.voting.vote import AnswerVote, VotingStatusEnum
from app.modules.q_a.answer.voting.vote_dto import AnswerVoteDto
from common.controllers.controller import Controller
from common.models import Reputation, User
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType, UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AnswerVoteController(Controller):
    def get(self, args, answer_id = None):
        """ Search votes.

        Args:
             The dictionary-like

        Returns
            A list of votes that satisfy conditions.
        """

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
        if user_id is None and answer_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide query parameters.')

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
            return send_result(data=marshal(votes, AnswerVoteDto.model_response), message='Success')
        else:
            return send_result(message='Answer vote not found')

    def get_by_id(self, object_id):
        if id is None:
            return send_error(message='Please provide id')
        vote = AnswerVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message='Answer vote not found')
        else:
            return send_result(data=marshal(vote, AnswerVoteDto.model_response), message='Success')

    def create(self, answer_id, data):
        current_user, _ = current_app.get_logged_user(request)
        # Check is admin or has permission
        if not (UserRole.is_admin(current_user.admin)
                or has_permission(current_user.id, PermissionType.ANSWER_VOTE)):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        if not isinstance(data, dict):
            return send_error(message='Wrong data format')
        data['user_id'] = current_user.id
        data['answer_id'] = answer_id
        try:
            # add or update vote
            is_insert = True
            old_vote_status = None
            vote = AnswerVote.query.filter(AnswerVote.user_id == data['user_id'], \
                AnswerVote.answer_id == data['answer_id']).first()
            if vote:
                old_vote_status = vote.vote_status
                is_insert = False
            vote = self._parse_vote(data=data, vote=vote)
            vote.created_date = datetime.utcnow()
            vote.updated_date = datetime.utcnow()
            if is_insert:
                db.session.add(vote)
            db.session.commit()
            if is_insert or (old_vote_status and old_vote_status != vote.vote_status):
                # update answer vote count in answer and user
                try:
                    answer = vote.voted_answer
                    # get user who was created answer and was voted
                    user_voted = answer.answer_by_user
                    for topic in answer.topics:
                        # Answer creator rep
                        reputation_creator = Reputation.query.filter(Reputation.user_id == user_voted.id, \
                            Reputation.topic_id == topic.id).first()
                        if reputation_creator is None:
                            reputation_creator = Reputation()
                            reputation_creator.user_id = user_voted.id
                            reputation_creator.topic_id = topic.id
                            reputation_creator.score = 0
                            db.session.add(reputation_creator)
                        # Answer voter rep
                        reputation_voter = Reputation.query.filter(Reputation.user_id == current_user.id, \
                            Reputation.topic_id == topic.id).first()
                        if reputation_voter is None:
                            reputation_voter = Reputation()
                            reputation_voter.user_id = user_voted.id
                            reputation_voter.topic_id = topic.id
                            reputation_voter.score = 0
                            db.session.add(reputation_voter)
                        # Set reputation score
                        if vote.vote_status == VotingStatusEnum.UPVOTED:
                            reputation_creator.score += 10
                        elif vote.vote_status == VotingStatusEnum.DOWNVOTED:
                            reputation_creator.score -= 2
                            reputation_voter.score -= 2
                        db.session.commit()
                except Exception as e:
                    print(e)
                    pass
            return send_result(data=marshal(vote, AnswerVoteDto.model_response), message='Success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message='Failed to create answer vote.')

    def delete(self, answer_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            vote = AnswerVote.query.filter_by(answer_id=answer_id, user_id=user_id).first()
            if vote is None:
                return send_error(message='Answer vote not found')
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Answer vote deleted successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete answer vote')

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
