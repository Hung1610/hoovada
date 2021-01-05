#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from sqlalchemy import event

# own modules
from common.db import db
from common.enum import VotingStatusEnum
from common.models.mixins import AuditCreateMixin, AuditUpdateMixin
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Reputation(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'reputation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table User
    score = db.Column(db.Float)

    @staticmethod
    def generate_score(target, value, oldvalue, initiator):
        Question = db.get_model('Question')
        Answer = db.get_model('Answer')
        AnswerVote = db.get_model('AnswerVote')
        Article = db.get_model('Article')
        ArticleVote = db.get_model('ArticleVote')
        Topic = db.get_model('Topic')

        # Calculate upvote score
        answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
            .filter(AnswerVote.answer.has(Answer.user_id == target.user_id) \
                & AnswerVote.answer.has(\
                    Answer.question.has(Question.topics.any(Topic.id == target.topic_id))) \
                & (AnswerVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
            .filter(ArticleVote.article.has(Article.user_id == target.user_id) \
                & ArticleVote.article.has(\
                    Article.topics.any(Topic.id == target.topic_id)) \
                & (ArticleVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()

        upvote_score = (answer_votes_count\
            + article_votes_count)\
            * 10

        # Calculate downvote score
        answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
            .filter((AnswerVote.answer.has(Answer.user_id == target.user_id) | (AnswerVote.user_id == target.user_id)) \
                & AnswerVote.answer.has(\
                    Answer.question.has(Question.topics.any(Topic.id == target.topic_id))) \
                & (AnswerVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
            .filter((ArticleVote.article.has(Article.user_id == target.user_id) | (ArticleVote.user_id == target.user_id)) \
                & ArticleVote.article.has(\
                    Article.topics.any(Topic.id == target.topic_id)) \
                & (ArticleVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        
        downvote_score = (answer_votes_count\
            + article_votes_count)\
            * (g.negative_rep_points)

        target.score = upvote_score + downvote_score

event.listen(Reputation.updated_date, 'set', Reputation.generate_score, retval=False)
