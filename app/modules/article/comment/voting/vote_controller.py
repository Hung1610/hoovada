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
from app.modules.article.comment.voting.vote_dto import ArticleCommentVoteDto
from common.controllers.controller import Controller
from common.enum import VotingStatusEnum
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Reputation = db.get_model('Reputation')
ArticleComment = db.get_model('ArticleComment')
ArticleCommentVote = db.get_model('ArticleCommentVote')


class ArticleCommentVoteController(Controller):
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

        query = ArticleCommentVote.query
        if user_id is not None:
            query = query.filter(ArticleCommentVote.user_id == user_id)
        if comment_id is not None:
            query = query.filter(ArticleCommentVote.comment_id == comment_id)
        if from_date is not None:
            query = query.filter(ArticleCommentVote.created_date >= from_date)
        if to_date is not None:
            query = query.filter(ArticleCommentVote.created_date <= to_date)
        votes = query.all()
        if votes is not None and len(votes) > 0:
            return send_result(data=marshal(votes, ArticleCommentVoteDto.model_response), message='Success')
        else:
            return send_result(message='ArticleComment vote not found')

    def get_by_id(self, object_id):
        if id is None:
            return send_error(message='Please provide id')
        vote = ArticleCommentVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message='ArticleComment vote not found')
        else:
            return send_result(data=marshal(vote, ArticleCommentVoteDto.model_response), message='Success')

    def create(self, comment_id, data):
        if not isinstance(data, dict):
            return send_error(message='Wrong data format')
        current_user, _ = current_app.get_logged_user(request)
        comment = ArticleComment.query.get(comment_id)
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
            vote = ArticleCommentVote.query.filter(ArticleCommentVote.user_id == data['user_id'], \
                ArticleCommentVote.comment_id == data['comment_id']).first()
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
                        # ArticleComment creator rep
                        reputation_creator = Reputation.query.filter(Reputation.user_id == user_voted.id, \
                            Reputation.topic_id == topic.id).first()
                        if reputation_creator is None:
                            reputation_creator = Reputation()
                            reputation_creator.user_id = user_voted.id
                            reputation_creator.topic_id = topic.id
                            db.session.add(reputation_creator)
                        # ArticleComment voter rep
                        reputation_voter = Reputation.query.filter(Reputation.user_id == current_user.id, \
                            Reputation.topic_id == topic.id).first()
                        if reputation_voter is None:
                            reputation_voter = Reputation()
                            reputation_voter.user_id = current_user.id
                            reputation_voter.topic_id = topic.id
                            db.session.add(reputation_voter)
                        # Set reputation score
                        reputation_creator.updated_date = datetime.now()
                        reputation_voter.updated_date = datetime.now()
                        db.session.commit()
                except Exception as e:
                    print(e)
                    pass
            return send_result(data=marshal(vote, ArticleCommentVoteDto.model_response), message='Success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message='Failed to create comment vote.')

    def delete(self, comment_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            vote = ArticleCommentVote.query.filter_by(comment_id=comment_id, user_id=user_id).first()
            if vote is None:
                return send_error(message='ArticleComment vote not found')
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='ArticleComment vote deleted successfully')
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
            vote = ArticleCommentVote()
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
