#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules

# third-party modules
from app.modules.q_a.question.question_controller import Question
from common.utils.onesignal_notif import push_notif_to_specific_users
import datetime
from common.enum import FrequencySettingEnum
from flask_dramatiq import Dramatiq
from flask import current_app, g
from flask.templating import render_template

# own modules
from common.utils.util import send_answer_notif_email, send_article_notif_email, send_email, send_question_notif_email
from common.db import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


dramatiq = Dramatiq()


@dramatiq.actor()
def test():
    print('THIS IS THE DEFAULT TASK MESSAGE')

@dramatiq.actor()
def send_weekly_registered_users():
    User = db.get_model('User')

    today_minus_one_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
    users = User.query.filter(User.joined_date > today_minus_one_week).all()

    html = render_template('admin_registered_users_notification.html', users=users)
    for admin_email in current_app.config['MAIL_ADMINS']:
        send_email(admin_email, 'Người dùng mới đăng ký -Hoovada', html)

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
def update_reputation(topic_id, voter_id):
    Reputation = db.get_model('Reputation')
    # Find reputation
    reputation_creator = Reputation.query.filter(Reputation.user_id == voter_id, Reputation.topic_id == topic_id).first()

    if reputation_creator is None:
        reputation_creator = Reputation()
        reputation_creator.user_id = voter_id
        reputation_creator.topic_id = topic_id
        db.session.add(reputation_creator)
    # Set reputation score
    reputation_creator.updated_date = datetime.datetime.now()

@dramatiq.actor()
def send_weekly_recommendation_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user_id in users:
        send_recommendation_mail.send(user_id[0])

@dramatiq.actor()
def send_daily_recommendation_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_recommendation_mail.send(user_id[0])

@dramatiq.actor()
def send_daily_similar_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_similar_mail.send(user_id[0])

@dramatiq.actor()
def send_weekly_similar_mails():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user_id in users:
        send_similar_mail.send(user_id[0])

@dramatiq.actor()
def send_recommendation_mail(user_id):
    Topic = db.get_model('Topic')
    TopicFollow = db.get_model('TopicFollow')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    User = db.get_model('User')
    user = User.query.get(user_id)
    if user.email:
        followed_topic_ids = [topic_id[0] for topic_id in TopicFollow.query.with_entities(TopicFollow.topic_id).filter(TopicFollow.user_id == user.id).all()]
        recommended_questions = Question.query.filter(Question.topics.any(Topic.id.in_(followed_topic_ids)))
        recommended_articles = Article.query.filter(Article.topics.any(Topic.id.in_(followed_topic_ids)))
        if (recommended_articles.count() + recommended_questions.count()) > 0:
            html = render_template('recommendation_for_user.html', \
                user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
            send_email(user.email, 'Món quà từ cộng đồng hoovada.com', html)

@dramatiq.actor()
def send_similar_mail(user_id):
    UserSeenQuestion = db.get_model('UserSeenQuestion')
    UserSeenArticle = db.get_model('UserSeenArticle')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    User = db.get_model('User')
    user = User.query.get(user_id)
    if user.email:
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
        recommended_questions = Question.query.filter(Question.id.in_(recommended_question_ids))

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
        recommended_articles = Article.query.filter(Article.id.in_(recommended_article_ids))
        
        
        if (recommended_articles.count() + recommended_questions.count()) > 0:
            html = render_template('similar_for_user.html', \
                user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
            send_email(user.email, 'Nội dung mà bạn quan tâm từ cộng đồng hoovada.com', html)

@dramatiq.actor()
def send_daily_new_topics():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user_id in users:
        send_new_topics.send(user_id[0])

@dramatiq.actor()
def send_weekly_new_topics():
    User = db.get_model('User')

    users = User.query.with_entities(User.id)\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

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
            send_email(user.email, 'Chủ đề mới từ cộng đồng hoovada.com', html)

@dramatiq.actor()
def new_article_notify_user_list(article_id, user_ids):
    User = db.get_model('User')
    Article = db.get_model('Article')

    users = User.query.with_entities(db.func.count(User.id))\
        .filter(User.id.in_(user_ids))\
        .scalar()

    article = Article.query.get(article_id)
    
    for user in users:
        if user.is_online:
            display_name =  article.user.display_name if article.user else 'Khách'
            message = '[Thông báo] ' + display_name + ' đã có bài viết mới!'
            push_notif_to_specific_users(message, [user.id])
        else:
            send_article_notif_email(user, article)

@dramatiq.actor()
def new_question_notify_user_list(question_id, user_ids):
    User = db.get_model('User')
    Question = db.get_model('Question')

    users = User.query.with_entities(db.func.count(User.id))\
        .filter(User.id.in_(user_ids))\
        .scalar()

    question = Question.query.get(question_id)
    
    for user in users:
        if user.is_online:
            display_name =  question.user.display_name if question.user else 'Khách'
            message = '[Thông báo] ' + display_name + ' đã có câu hỏi mới!'
            push_notif_to_specific_users(message, [user.id])
        else:
            send_question_notif_email(user, question)

@dramatiq.actor()
def new_answer_notify_user_list(answer_id, user_ids):
    User = db.get_model('User')
    Answer = db.get_model('Answer')

    users = User.query.with_entities(db.func.count(User.id))\
        .filter(User.id.in_(user_ids))\
        .scalar()

    answer = Answer.query.get(answer_id)
    
    for user in users:
        if user.is_online:
            display_name =  answer.user.display_name if answer.user else 'Khách'
            message = '[Thông báo] ' + display_name + ' đã có câu trả lời mới!'
            push_notif_to_specific_users(message, [user.id])
        else:
            send_answer_notif_email(user, answer, answer.question)