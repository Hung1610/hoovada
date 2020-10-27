#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request, current_app
from flask_restx import marshal

# own modules
from app import db
from common.controllers.controller import Controller
from common.models import AnswerComment
from app.modules.q_a.answer.comment.voting.vote import AnswerCommentVote, VotingStatusEnum
from app.modules.q_a.answer.comment.voting.vote_dto import AnswerCommentVoteDto
from common.models import User
from common.models import Reputation
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AnswerCommentVoteController(Controller):
    def get(self, args, comment_id = None):
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
        if user_id is None and comment_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide query parameters.')

        query = AnswerCommentVote.query
        if user_id is not None:
            query = query.filter(AnswerCommentVote.user_id == user_id)
        if comment_id is not None:
            query = query.filter(AnswerCommentVote.comment_id == comment_id)
        if from_date is not None:
            query = query.filter(AnswerCommentVote.created_date >= from_date)
        if to_date is not None:
            query = query.filter(AnswerCommentVote.created_date <= to_date)
        votes = query.all()
        if votes is not None and len(votes) > 0:
            return send_result(data=marshal(votes, AnswerCommentVoteDto.model_response), message='Success')
        else:
            return send_result(message='AnswerComment vote not found')

    def get_by_id(self, object_id):
        if id is None:
            return send_error(message='Please provide id')
        vote = AnswerCommentVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message='AnswerComment vote not found')
        else:
            return send_result(data=marshal(vote, AnswerCommentVoteDto.model_response), message='Success')

    def create(self, comment_id, data):
        if not isinstance(data, dict):
            return send_error(message='Wrong data format')
        current_user, _ = current_app.get_logged_user(request)
        comment = AnswerComment.query.get(comment_id)
        if not comment:
            return send_error(message='Comment not found.')
        if not comment.allow_favorite:
            return send_error(message='Comment does not allow voting.')
        data['user_id'] = current_user.id
        data['comment_id'] = comment_id
        try:
            # add or update vote
            is_insert = True
            old_vote_status = None
            vote = AnswerCommentVote.query.filter(AnswerCommentVote.user_id == data['user_id'], \
                AnswerCommentVote.comment_id == data['comment_id']).first()
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
                # update comment vote count in comment and user
                try:
                    comment = vote.voted_comment
                    # get user who was created comment and was voted
                    user_voted = comment.comment_by_user
                    for topic in comment.topics:
                        # AnswerComment creator rep
                        reputation_creator = Reputation.query.filter(Reputation.user_id == user_voted.id, \
                            Reputation.topic_id == topic.id).first()
                        if reputation_creator is None:
                            reputation_creator = Reputation()
                            reputation_creator.user_id = user_voted.id
                            reputation_creator.topic_id = topic.id
                            reputation_creator.score = 0
                            db.session.add(reputation_creator)
                        # AnswerComment voter rep
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
            return send_result(data=marshal(vote, AnswerCommentVoteDto.model_response), message='Success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message='Failed to create comment vote.')

    def delete(self, comment_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            vote = AnswerCommentVote.query.filter_by(comment_id=comment_id, user_id=user_id).first()
            if vote is None:
                return send_error(message='AnswerComment vote not found')
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='AnswerComment vote deleted successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Failed to delete comment vote')

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
            vote = AnswerCommentVote()
        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in data:
             try:
                 vote.comment_id = int(data['comment_id'])
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
