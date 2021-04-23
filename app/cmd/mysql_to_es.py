#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import environ
from datetime import datetime
from flask import current_app
from elasticsearch_dsl import connections
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk


from sqlalchemy import create_engine

# mysql configuration
DB_USER = environ.get('DB_USER', 'admin')
DB_PASSWORD = environ.get('DB_PASSWORD', 'admin')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_PORT = environ.get('DB_PORT', '3306')
DB_NAME = environ.get('DB_NAME', 'hoovada')
DB_CHARSET = 'utf8mb4'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    name=DB_NAME,
    charset=DB_CHARSET
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
connection = engine.connect()

connections.create_connection(hosts=['localhost'], timeout=20)

# ES models


class Article(Document):
    id = Integer()
    html = Text()
    title = Text(fields={'raw': Keyword()})
    user_id = Integer()
    slug = Text(fields={'raw': Keyword()})
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "article"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

class Post(Document):
    id = Integer()
    html = Text()
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "post"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

class Question(Document):
    id = Integer()
    question = Text()
    title = Text(fields={'raw': Keyword()})
    user_id = Integer()
    slug = Text(fields={'raw': Keyword()})
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "question"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

class Topic(Document):
    id = Integer()
    html = Text()
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "topic"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

class User(Document):
    id = Integer()
    display_name = Text(analyzer='standard', fields={'raw': Keyword()})
    email = Text(analyzer='standard', fields={'raw': Keyword()})
    gender = Text(fields={'raw': Keyword()})
    age = Integer()
    last_name = Text(analyzer='standard', fields={'raw': Keyword()})
    first_name = Text(analyzer='standard', fields={'raw': Keyword()})
    middle_name = Text(analyzer='standard', fields={'raw': Keyword()})
    reputation = Integer()

    class Index:
        name = "user"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

def create_indexes():
    User.init()
    Post.init()
    Topic.init()
    Article.init()
    Question.init()


def migrate_user_model():
    query = "SELECT id, display_name, email, gender, age, reputation, first_name, middle_name, last_name  from user"
    res = connection.execute(query).fetchall()
    list_users = []
    for user in res:
        (user_id, display_name, email, gender, age, reputation, first_name, middle_name, last_name) = user
        user_dsl = User(_id=user_id, display_name=display_name, email=email,
             gender=gender, age=age, reputation=reputation, first_name=first_name, middle_name=middle_name, last_name=last_name)
        list_users.append(user_dsl)
    bulk(connections.get_connection(), (d.to_dict(True) for d in list_users))

def migrate_question_model():
    query = "SELECT id, question, title, user_id, slug, created_date, updated_date from question"
    res = connection.execute(query).fetchall()
    list_questions = []
    for _question in res:
        (question_id, question, title, user_id, slug, created_date, updated_date) = _question
        question_dsl = Question(_id=question_id, question=question, title=title, user_id=user_id, slug=slug, created_date=created_date, updated_date=updated_date)
        list_questions.append(question_dsl)
    bulk(connections.get_connection(), (d.to_dict(True) for d in list_questions))


def migrate_article_model():
    query = "SELECT id, html, title, user_id, slug, created_date, updated_date from article"
    res = connection.execute(query).fetchall()
    list_articles = []
    for article in res:
        (article_id, html, title, user_id, slug, created_date, updated_date) = article
        article_dsl = Article(_id=article_id, html=html, title=title, user_id=user_id, slug=slug, created_date=created_date, updated_date=updated_date)
        list_articles.append(article_dsl)
    bulk(connections.get_connection(), (d.to_dict(True) for d in list_articles))

def migrate_topic_model():
    query = "SELECT id, description, user_id, name, slug,is_fixed, created_date from topic"
    res = connection.execute(query).fetchall()
    list_topics = []
    for topic in res:
        (topic_id, description, user_id, name, slug,is_fixed, created_date) = topic
        topic_dsl = Topic(_id=topic_id, description=description, user_id=user_id, name=name, slug=slug, is_fixed=is_fixed, created_date=created_date)
        list_topics.append(topic_dsl)
    bulk(connections.get_connection(), (d.to_dict(True) for d in list_topics))

def migrate_post_model():
    query = "SELECT id, html, user_id, created_date, updated_date from post"
    res = connection.execute(query).fetchall()
    list_posts = []
    for post in res:
        (post_id, html, user_id, created_date, updated_date) = post
        post_dsl = Post(_id=post_id, html=html, user_id=user_id, created_date=created_date, updated_date=updated_date)
        list_posts.append(post_dsl)
    bulk(connections.get_connection(), (d.to_dict(True) for d in list_posts))

def main():
    create_indexes()
    migrate_user_model()
    migrate_question_model()
    migrate_article_model()
    migrate_topic_model()
    migrate_post_model()

main()