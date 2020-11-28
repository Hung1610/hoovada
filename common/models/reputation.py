#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from sqlalchemy import event

# own modules
from app.app import db
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
        QuestionVote = db.get_model('QuestionVote')
        QuestionComment = db.get_model('QuestionComment')
        QuestionCommentVote = db.get_model('QuestionCommentVote')
        Answer = db.get_model('Answer')
        AnswerVote = db.get_model('AnswerVote')
        AnswerComment = db.get_model('AnswerComment')
        AnswerCommentVote = db.get_model('AnswerCommentVote')
        Article = db.get_model('Article')
        ArticleVote = db.get_model('ArticleVote')
        ArticleComment = db.get_model('ArticleComment')
        ArticleCommentVote = db.get_model('ArticleCommentVote')
        Topic = db.get_model('Topic')

        # Calculate upvote score
        question_votes_count = QuestionVote.query.with_entities(db.func.count(QuestionVote.id))\
            .filter(QuestionVote.question.has(Question.user_id == target.user_id) \
                & (QuestionVote.question.has(\
                    Question.topics.any(Topic.id == target.topic_id))) \
                & (QuestionVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        question_comment_votes_count = QuestionCommentVote.query.with_entities(db.func.count(QuestionCommentVote.id))\
            .filter(QuestionCommentVote.comment.has(QuestionComment.user_id == target.user_id) \
                & QuestionCommentVote.comment.has(\
                    QuestionComment.question.has(\
                        Question.topics.any(Topic.id == target.topic_id))) \
                & (QuestionCommentVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
            .filter(AnswerVote.answer.has(Answer.user_id == target.user_id) \
                & AnswerVote.answer.has(\
                    Answer.question.has(Question.topics.any(Topic.id == target.topic_id))) \
                & (AnswerVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        answer_comment_votes_count = AnswerCommentVote.query.with_entities(db.func.count(AnswerCommentVote.id))\
            .filter(AnswerCommentVote.comment.has(AnswerComment.user_id == target.user_id) \
                & AnswerCommentVote.comment.has(\
                    AnswerComment.answer.has(\
                        Answer.question.has(Question.topics.any(Topic.id == target.topic_id)))) \
                & (AnswerCommentVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
            .filter(ArticleVote.article.has(Article.user_id == target.user_id) \
                & ArticleVote.article.has(\
                    Article.topics.any(Topic.id == target.topic_id)) \
                & (ArticleVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()
        article_comment_votes_count = ArticleCommentVote.query.with_entities(db.func.count(ArticleCommentVote.id))\
            .filter(ArticleCommentVote.comment.has(ArticleComment.user_id == target.user_id) \
                & ArticleCommentVote.comment.has(\
                    ArticleComment.article.has(\
                        Article.topics.any(Topic.id == target.topic_id))) \
                & (ArticleCommentVote.vote_status == VotingStatusEnum.UPVOTED.name))\
            .scalar()

        upvote_score = (question_votes_count + question_comment_votes_count\
            + answer_votes_count + answer_comment_votes_count\
            + article_votes_count + article_comment_votes_count)\
            * 10

        # Calculate downvote score
        question_votes_count = QuestionVote.query.with_entities(db.func.count(QuestionVote.id))\
            .filter((QuestionVote.question.has(Question.user_id == target.user_id) | QuestionVote.user_id == target.user_id) \
                & QuestionVote.question.has(\
                    Question.topics.any(Topic.id == target.topic_id)) \
                & (QuestionVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        question_comment_votes_count = QuestionCommentVote.query.with_entities(db.func.count(QuestionCommentVote.id))\
            .filter((QuestionCommentVote.comment.has(QuestionComment.user_id == target.user_id) | QuestionCommentVote.user_id == target.user_id) \
                & QuestionCommentVote.comment.has(\
                    QuestionComment.question.has(\
                        Question.topics.any(Topic.id == target.topic_id))) \
                & (QuestionCommentVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
            .filter((AnswerVote.answer.has(Answer.user_id == target.user_id) | AnswerVote.user_id == target.user_id) \
                & AnswerVote.answer.has(\
                    Answer.question.has(Question.topics.any(Topic.id == target.topic_id))) \
                & (AnswerVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        answer_comment_votes_count = AnswerCommentVote.query.with_entities(db.func.count(AnswerCommentVote.id))\
            .filter((AnswerCommentVote.comment.has(AnswerComment.user_id == target.user_id) | AnswerCommentVote.user_id == target.user_id) \
                & AnswerCommentVote.comment.has(\
                    AnswerComment.answer.has(\
                        Answer.question.has(Question.topics.any(Topic.id == target.topic_id)))) \
                & (AnswerCommentVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
            .filter((ArticleVote.article.has(Article.user_id == target.user_id) | ArticleVote.user_id == target.user_id) \
                & ArticleVote.article.has(\
                    Article.topics.any(Topic.id == target.topic_id)) \
                & (ArticleVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        article_comment_votes_count = ArticleCommentVote.query.with_entities(db.func.count(ArticleCommentVote.id))\
            .filter((ArticleCommentVote.comment.has(ArticleComment.user_id == target.user_id) | ArticleCommentVote.user_id == target.user_id) \
                & ArticleCommentVote.comment.has(\
                    ArticleComment.article.has(\
                        Article.topics.any(Topic.id == target.topic_id))) \
                & (ArticleCommentVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
            .scalar()
        
        downvote_score = (question_votes_count + question_comment_votes_count\
            + answer_votes_count + answer_comment_votes_count\
            + article_votes_count + article_comment_votes_count)\
            * (-2)

        target.score = upvote_score + downvote_score

event.listen(Reputation.updated_date, 'set', Reputation.generate_score, retval=False)
