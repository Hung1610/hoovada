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
from common.models.model import db
from app.modules.article.voting import constants
from app.modules.article.voting.vote_dto import VoteDto
from common.controllers.controller import Controller
from common.models import Reputation, User
from common.models.vote import ArticleVote, VotingStatusEnum
from common.utils.permission import has_permission
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class VoteController(Controller):
    def get(self, args, article_id = None):
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
        if user_id is None and article_id is None and from_date is None and to_date is None:
            return send_error(message=constants.msg_lacking_query_params)

        query = ArticleVote.query
        if user_id is not None:
            query = query.filter(ArticleVote.user_id == user_id)
        if article_id is not None:
            query = query.filter(ArticleVote.article_id == article_id)
        if from_date is not None:
            query = query.filter(ArticleVote.created_date >= from_date)
        if to_date is not None:
            query = query.filter(ArticleVote.created_date <= to_date)
        votes = query.all()
        if votes is not None and len(votes) > 0:
            return send_result(data=marshal(votes, VoteDto.model_response), message='Success')
        else:
            return send_result(message=constants.msg_vote_not_found)

    def get_by_id(self, object_id):
        if id is None:
            return send_error(message=constants.msg_lacking_id)
        vote = ArticleVote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message=constants.msg_vote_not_found)
        else:
            return send_result(data=marshal(vote, VoteDto.model_response), message='Success')

    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)
        current_user, _ = current_app.get_logged_user(request)
        if not has_permission(current_user.id, PermissionType.VOTE):
            return send_error(code=401, message='You have no authority to perform this action')
        article = db.get_model('Article').query.get(article_id)
        if not article:
            return send_error(message='Article not found')
        if not article.allow_voting:
            return send_error(message='Article does not allow voting')
        data['user_id'] = current_user.id
        data['article_id'] = article_id
        try:
            # add or update vote
            is_insert = True
            old_vote_status = None
            vote = ArticleVote.query.filter(ArticleVote.user_id == data['user_id'], \
                ArticleVote.article_id == data['article_id']).first()
            if vote:
                old_vote_status = vote.vote_status
                is_insert = False
            vote = self._parse_vote(data=data, vote=vote)
            vote.created_date = datetime.utcnow()
            vote.updated_date = datetime.utcnow()
            if is_insert:
                db.session.add(vote)
            db.session.commit()
            article = vote.article
            # get user who was created article and was voted
            user_voted = article.user
            for topic in article.topics:
                # Article creator rep
                update_reputation.send(topic.id, user_voted.id)
                # Article voter rep
                update_reputation.send(topic.id, current_user.id)
            db.session.commit()
            return send_result(data=marshal(vote, VoteDto.model_response), message='Success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=constants.msg_create_failed.format(e))

    def delete(self, article_id):
        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id
        try:
            vote = ArticleVote.query.filter_by(article_id=article_id, user_id=user_id).first()
            if vote is None:
                return send_error(message=constants.msg_vote_not_found)
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(vote.id))
        except Exception as e:
            print(e.__str__())
            return send_error(message=constants.msg_delete_failed)

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
            vote = ArticleVote()
        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'article_id' in data:
             try:
                 vote.article_id = int(data['article_id'])
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
