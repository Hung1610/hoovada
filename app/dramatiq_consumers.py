#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules

# third-party modules
from flask_dramatiq import Dramatiq
from flask import current_app, g
from flask.templating import render_template

# own modules
from common.utils.util import send_email
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
def send_recommendation_mail(user):
    Topic = db.get_model('Topic')
    TopicFollow = db.get_model('TopicFollow')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    if user.email:
        followed_topic_ids = TopicFollow.query.with_entities(TopicFollow.topic_id).filter(TopicFollow.user_id == user.id).all()
        recommended_questions = Question.query.filter(Question.topics.any(Topic.id.in_(followed_topic_ids)))
        recommended_articles = Article.query.filter(Article.topics.any(Topic.id.in_(followed_topic_ids)))
        html = render_template('recommendation_for_user.html', \
            user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
        send_email(user.email, 'Recommended Questions and Articles On Hoovada', html)

@dramatiq.actor()
def send_similar_mail(user):
    UserSeenQuestion = db.get_model('UserSeenQuestion')
    UserSeenArticle = db.get_model('UserSeenArticle')
    Question = db.get_model('Question')
    Article = db.get_model('Article')
    if user.email:
        seen_question_ids = UserSeenQuestion.query\
            .with_entities(UserSeenQuestion.question_id)\
            .filter(UserSeenQuestion.user_id == user.id)\
            .order_by(db.asc(UserSeenQuestion.created_date))\
            .distinct()
        recommended_question_ids = {}
        for seen_question_id in seen_question_ids:
            seen_question = Question.query.get(seen_question_id)
            title_similarity = db.func.SIMILARITY_STRING(db.text('title'), seen_question.title).label('title_similarity')
            questions = Question.query.with_entities(Question.id)\
                .filter(Question.id != seen_question_id)\
                .filter(Question.is_private == False)\
                .filter(title_similarity > 75)\
                .order_by(db.desc(title_similarity))\
                .limit(10)\
                .all()
            recommended_question_ids.update(questions)
        recommended_questions = Question.query.filter(Question.id.in_(recommended_question_ids))

        seen_article_ids = UserSeenArticle.query\
            .with_entities(UserSeenArticle.article_id)\
            .filter(UserSeenArticle.user_id == user.id)\
            .order_by(db.asc(UserSeenArticle.created_date))\
            .distinct()
        recommended_article_ids = {}
        for seen_article_id in seen_article_ids:
            seen_article = Article.query.get(seen_article_id)
            title_similarity = db.func.SIMILARITY_STRING(db.text('title'), seen_article.title).label('title_similarity')
            articles = Article.query.with_entities(Article.id)\
                .filter(Article.id != seen_article_id)\
                .filter(title_similarity > 75)\
                .order_by(db.desc(title_similarity))\
                .limit(10)\
                .all()
            recommended_article_ids.update(articles)
        recommended_articles = Article.query.filter(Article.id.in_(recommended_article_ids))
        

        html = render_template('similar_for_user.html', \
            user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
        send_email(user.email, 'Similar Questions and Articles On Hoovada', html)