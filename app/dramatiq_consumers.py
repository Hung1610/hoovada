#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
import datetime

# third-party modules
from flask import current_app, render_template
from flask_dramatiq import Dramatiq

# own modules
from common.db import db
from common.enum import FrequencySettingEnum, VotingStatusEnum
from common.utils.onesignal_notif import push_notif_to_specific_users
from common.utils.util import send_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


dramatiq = Dramatiq()


@dramatiq.actor(actor_name='test', queue_name='app_queue')
def test():
    print('THIS IS THE DEFAULT TASK MESSAGE', flush=True)

@dramatiq.actor()
def send_weekly_registered_users():
    User = db.get_model('User')

    today_minus_one_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    users = User.query.filter(User.joined_date > today_minus_one_week).all()

    html = render_template('admin_registered_users_notification.html', users=users)
    for admin_email in current_app.config['MAIL_ADMINS']:
        send_email(admin_email, 'Người dùng mới đăng ký tham gia công đồng hoovada.com', html)

@dramatiq.actor()
def update_seen_questions(question_id, user_id):
    UserSeenQuestion = db.get_model('UserSeenQuestion')

    seen_count = UserSeenQuestion.query.with_entities(db.func.count(UserSeenQuestion.id))\
        .filter(UserSeenQuestion.user_id == user_id)\
        .scalar()
    
    if seen_count > current_app.config['MAX_SEEN_CACHE']:
        oldest_cache = UserSeenQuestion.query\
            .filter(UserSeenQuestion.user_id == user_id)\
            .order_by(db.asc(UserSeenQuestion.created_date))\
            .first()
        db.session.delete(oldest_cache)
    
    new_cache = UserSeenQuestion()
    new_cache.user_id = user_id
    new_cache.question_id = question_id
    db.session.add(new_cache)
    db.session.commit()
        
@dramatiq.actor()
def update_seen_poll(user_id, poll_id):
    UserSeenPoll = db.get_model('UserSeenPoll')

    seen_count = UserSeenPoll.query.with_entities(db.func.count(UserSeenPoll.id))\
        .filter(UserSeenPoll.user_id == user_id)\
        .scalar()
    
    if seen_count > current_app.config['MAX_SEEN_CACHE']:
        oldest_cache = UserSeenPoll.query\
            .filter(UserSeenPoll.user_id == user_id)\
            .order_by(db.asc(UserSeenPoll.created_date))\
            .first()
        db.session.delete(oldest_cache)
    
    new_cache = UserSeenPoll()
    new_cache.user_id = user_id
    new_cache.poll_id = poll_id
    db.session.add(new_cache)
    db.session.commit()

@dramatiq.actor()
def update_seen_articles(article_id, user_id):
    UserSeenArticle = db.get_model('UserSeenArticle')

    seen_count = UserSeenArticle.query.with_entities(db.func.count(UserSeenArticle.id))\
        .filter(UserSeenArticle.user_id == user_id)\
        .scalar()
    
    if seen_count > current_app.config['MAX_SEEN_CACHE']:
        oldest_cache = UserSeenArticle.query\
            .filter(UserSeenArticle.user_id == user_id)\
            .order_by(db.asc(UserSeenArticle.created_date))\
            .first()
        db.session.delete(oldest_cache)
    
    new_cache = UserSeenArticle()
    new_cache.user_id = user_id
    new_cache.article_id = article_id
    db.session.add(new_cache)
    db.session.commit()

@dramatiq.actor()
def update_reputation(topic_id, voter_id, is_voter=False):
    Reputation = db.get_model('Reputation')
    User = db.get_model('User')
    Question = db.get_model('Question')
    Answer = db.get_model('Answer')
    AnswerVote = db.get_model('AnswerVote')
    Article = db.get_model('Article')
    ArticleVote = db.get_model('ArticleVote')
    Topic = db.get_model('Topic')

    if is_voter:
        negative_rep_points = -1
    else:
        negative_rep_points = -2

    # Find reputation
    reputation_creator = Reputation.query.filter(Reputation.user_id == voter_id, Reputation.topic_id == topic_id).first()

    if reputation_creator is None:
        reputation_creator = Reputation()
        reputation_creator.user_id = voter_id
        reputation_creator.topic_id = topic_id
        db.session.add(reputation_creator)
        
    # Set reputation score
    # Calculate upvote score
    answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
        .filter(AnswerVote.answer.has(Answer.user_id == reputation_creator.user_id) \
            & AnswerVote.answer.has(\
                Answer.question.has(Question.topics.any(Topic.id == reputation_creator.topic_id))) \
            & (AnswerVote.vote_status == VotingStatusEnum.UPVOTED.name))\
        .scalar()
    article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
        .filter(ArticleVote.article.has(Article.user_id == reputation_creator.user_id) \
            & ArticleVote.article.has(\
                Article.topics.any(Topic.id == reputation_creator.topic_id)) \
            & (ArticleVote.vote_status == VotingStatusEnum.UPVOTED.name))\
        .scalar()

    upvote_score = (answer_votes_count\
        + article_votes_count)\
        * 10

    # Calculate downvote score
    answer_votes_count = AnswerVote.query.with_entities(db.func.count(AnswerVote.id))\
        .filter((AnswerVote.answer.has(Answer.user_id == reputation_creator.user_id) | (AnswerVote.user_id == reputation_creator.user_id)) \
            & AnswerVote.answer.has(\
                Answer.question.has(Question.topics.any(Topic.id == reputation_creator.topic_id))) \
            & (AnswerVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
        .scalar()
    article_votes_count = ArticleVote.query.with_entities(db.func.count(ArticleVote.id))\
        .filter((ArticleVote.article.has(Article.user_id == reputation_creator.user_id) | (ArticleVote.user_id == reputation_creator.user_id)) \
            & ArticleVote.article.has(\
                Article.topics.any(Topic.id == reputation_creator.topic_id)) \
            & (ArticleVote.vote_status == VotingStatusEnum.DOWNVOTED.name))\
        .scalar()
    
    downvote_score = (answer_votes_count\
        + article_votes_count)\
        * negative_rep_points

    reputation_creator.score = upvote_score + downvote_score
    db.session.commit()

    total_rep = Reputation.query.with_entities(db.func.sum(Reputation.score))\
       .filter(Reputation.user_id == voter_id)\
       .scalar()

    user = User.query.get(voter_id)
    user.reputation = total_rep
    db.session.commit()


@dramatiq.actor()
def send_weekly_recommendation_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user_id in users:
        send_recommendation_mail.send(user_id[0])

@dramatiq.actor()
def send_daily_recommendation_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_recommendation_mail.send(user_id[0])

@dramatiq.actor()
def send_daily_similar_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_similar_mail.send(user_id[0])

@dramatiq.actor()
def send_weekly_similar_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user_id in users:
        send_similar_mail.send(user_id[0])

@dramatiq.actor()
def send_recommendation_mail(user_id):
    UserMailedQuestion = db.get_model('UserMailedQuestion')
    UserMailedArticle = db.get_model('UserMailedArticle')
    Topic = db.get_model('Topic')
    TopicFollow = db.get_model('TopicFollow')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    User = db.get_model('User')
    user = User.query.get(user_id)
    if user.email:
        today_minus_one_month = datetime.datetime.now() - datetime.timedelta(weeks=4)
        mailed_question_ids = [question[0] for question in UserMailedQuestion.query\
            .with_entities(UserMailedQuestion.question_id)\
            .distinct()\
            .filter(UserMailedQuestion.created_date > today_minus_one_month)]
        mailed_article_ids = [article[0] for article in UserMailedArticle.query\
            .with_entities(UserMailedArticle.article_id)\
            .distinct()\
            .filter(UserMailedArticle.created_date > today_minus_one_month)]
        
        followed_topic_ids = [topic_id[0] for topic_id in \
            TopicFollow.query.with_entities(TopicFollow.topic_id).filter(TopicFollow.user_id == user.id).all()]

        recommended_questions = Question.query\
            .filter(~Question.id.in_(mailed_question_ids))\
            .filter(Question.topics.any(Topic.id.in_(followed_topic_ids)))
        recommended_articles = Article.query\
            .filter(~Article.id.in_(mailed_article_ids))\
            .filter(Article.topics.any(Topic.id.in_(followed_topic_ids)))

        if (recommended_articles.count() + recommended_questions.count()) > 0:
            db.session.add_all([\
                UserMailedQuestion(user_id=user.id, question_id=question.id) for question in recommended_questions])
            db.session.add_all([\
                UserMailedArticle(user_id=user.id, article_id=article.id) for article in recommended_articles])
            db.session.commit()
            html = render_template('recommendation_for_user.html', \
                user=user, recommended_articles=recommended_articles, recommended_questions=recommended_questions)
            send_email(user.email, 'Hoovada - Nội dung mà bạn có thể quan tâm!', html)

@dramatiq.actor()
def send_similar_mail(user_id):
    UserMailedQuestion = db.get_model('UserMailedQuestion')
    UserMailedArticle = db.get_model('UserMailedArticle')
    UserSeenQuestion = db.get_model('UserSeenQuestion')
    UserSeenArticle = db.get_model('UserSeenArticle')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    User = db.get_model('User')
    user = User.query.get(user_id)
    if user.email:
        today_minus_one_month = datetime.datetime.now() - datetime.timedelta(weeks=4)
        mailed_question_ids = [question[0] for question in UserMailedQuestion.query\
            .with_entities(UserMailedQuestion.question_id)\
            .distinct()\
            .filter(UserMailedQuestion.created_date > today_minus_one_month)]
        mailed_article_ids = [article[0] for article in UserMailedArticle.query\
            .with_entities(UserMailedArticle.article_id)\
            .distinct()\
            .filter(UserMailedArticle.created_date > today_minus_one_month)]

        seen_question_ids = UserSeenQuestion.query\
            .with_entities(UserSeenQuestion.question_id)\
            .filter(UserSeenQuestion.user_id == user.id)\
            .order_by(db.asc(UserSeenQuestion.created_date))\
            .distinct()
        recommended_question_ids = set()
        for seen_question_id in seen_question_ids:
            seen_question = Question.query.get(seen_question_id[0])
            title_similarity = db.func.SIMILARITY_STRING(db.text('title'), seen_question.title).label('title_similarity')
            questions = Question.query.with_entities(Question.id)\
                .filter(Question.id != seen_question_id[0])\
                .filter(Question.is_private == False)\
                .filter(title_similarity > 75)\
                .order_by(db.desc(title_similarity))\
                .limit(10)\
                .all()
            recommended_question_ids.update([question[0] for question in questions])
        recommended_questions = Question.query\
            .filter(~Question.id.in_(mailed_question_ids))\
            .filter(Question.id.in_(recommended_question_ids))

        seen_article_ids = UserSeenArticle.query\
            .with_entities(UserSeenArticle.article_id)\
            .filter(UserSeenArticle.user_id == user.id)\
            .order_by(db.asc(UserSeenArticle.created_date))\
            .distinct()
        recommended_article_ids = set()
        for seen_article_id in seen_article_ids:
            seen_article = Article.query.get(seen_article_id[0])
            title_similarity = db.func.SIMILARITY_STRING(db.text('title'), seen_article.title).label('title_similarity')
            articles = Article.query.with_entities(Article.id)\
                .filter(Article.id != seen_article_id[0])\
                .filter(title_similarity > 75)\
                .order_by(db.desc(title_similarity))\
                .limit(10)\
                .all()
            recommended_article_ids.update([article[0] for article in articles])
        
        recommended_articles = Article.query\
            .filter(~Article.id.in_(mailed_article_ids))\
            .filter(Article.id.in_(recommended_article_ids))
        if (recommended_articles.count() + recommended_questions.count()) > 0:
            db.session.add_all([\
                UserMailedQuestion(user_id=user.id, question_id=question.id) for question in recommended_questions])
            db.session.add_all([\
                UserMailedArticle(user_id=user.id, article_id=article.id) for article in recommended_articles])
            db.session.commit()
            html = render_template('similar_for_user.html', user=user, recommended_articles=recommended_articles, recommended_questions=recommended_questions)
            
            send_email(user.email, 'Hoovada - Nội dung mà bạn có thể quan tâm!', html)

@dramatiq.actor()
def send_daily_new_topics():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_new_topics.send(user_id[0])

@dramatiq.actor()
def send_weekly_new_topics():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.is_deactivated == False, User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user_id in users:
        send_new_topics.send(user_id[0])

@dramatiq.actor()
def send_new_topics(user_id):
    Topic = db.get_model('Topic')
    User = db.get_model('User')

    user = User.query.get(user_id)

    today_minus_one_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    topics = Topic.query.filter(Topic.created_date > today_minus_one_week).all()

    if topics.count() > 0:
        html = render_template('new_topics.html', user=user, topics=topics)
        if user.email:
            send_email(user.email, 'Hoovada - Chủ đề mới', html)