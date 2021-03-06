#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import environ
from datetime import datetime
from flask import current_app
from elasticsearch_dsl import connections
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter, Index, Q
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from io import StringIO
from html.parser import HTMLParser

from sqlalchemy import create_engine

# mysql configuration
DB_USER = environ.get('DB_USER', 'admin')
DB_PASSWORD = environ.get('DB_PASSWORD', 'admin')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_PORT = environ.get('DB_PORT', '3306')
DB_NAME = environ.get('DB_NAME', 'hoovada')
DB_CHARSET = 'utf8mb4'

# ES configuration
ES_HOST = environ.get('ES_HOST', 'localhost')
ES_TIMEOUT = environ.get('ES_TIMEOUT', 20)
ES_USER = environ.get('ES_USER', 'user')
ES_PASSWORD = environ.get('ES_PASSWORD', 'password')


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

connections.create_connection(hosts=[ES_HOST], timeout=ES_TIMEOUT, http_auth=(ES_USER, ES_PASSWORD))

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# ES custom analyzers

# vn_text_analyzer = analyzer('vn_text_analyzer',
#     tokenizer='vi_tokenizer',
#     filter=['icu_folding']
# )

# ES models
article_index = Index('article')
@article_index.document
class Article(Document):
    id = Integer()
    html = Text(analyzer='standard')
    title = Text(analyzer='standard', fields={'raw': Keyword()})
    user_id = Integer()
    slug = Text(analyzer='standard', fields={'raw': Keyword()})
    created_date = Date()
    updated_date = Date()

post_index = Index('post')
@post_index.document
class Post(Document):
    id = Integer()
    html = Text(analyzer='standard')
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

question_index = Index('question')
@question_index.document
class Question(Document):
    id = Integer()
    question = Text(analyzer='standard')
    title = Text(analyzer='standard')
    user_id = Integer()
    slug = Text(analyzer='standard')
    created_date = Date()
    updated_date = Date()

topic_index = Index('topic')
@topic_index.document
class Topic(Document):
    id = Integer()
    description = Text(analyzer='standard')
    name = Text(analyzer='standard')
    slug= Text(analyzer='standard')
    is_fixed = Integer()
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

user_index = Index('user')
@user_index.document
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

poll_index = Index("poll")
@poll_index.document
class Poll(Document):
    id = Integer()
    title = Text(analyzer='standard')
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

user_friend_index = Index('user_friend')
@user_friend_index.document
class UserFriend(Document):
    friend_id = Integer()
    friended_id = Integer()
    friend_display_name = Text(analyzer='standard')
    friend_email = Text(analyzer='standard')
    friend_profile_pic_url = Text()
    friended_display_name = Text(analyzer='standard')
    friended_email = Text(analyzer='standard')
    friended_profile_pic_url = Text()
    is_approved = Integer()

def delete_index_if_exist(model_index):
    if model_index.exists() == True:
        model_index.delete()
    model_index.create()
    model_index.analyzer('standard')

def select_with_pagination(query, limit=0, offset=0):
    return connection.execute(query + " LIMIT {} OFFSET {}".format(limit, offset)).fetchall()

def select_one(table, id):
    rows = connection.execute('SELECT * FROM {} WHERE id = "{}"'.format(table, id)).fetchall()
    if not rows or len(rows) == 0:
        return None
    return rows[0]

BATCH_SIZE = 100

def migrate_user_friend_model():
    query = "SELECT id, friend_id, friended_id, is_approved from user_friend"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting friend migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_friends = []
        for user_friend in res:
            (user_friend_id, friend_id, friended_id, is_approved) = user_friend
            friend = select_one("user", friend_id)
            friended = select_one("user", friended_id)
            if friend is None or friended is None:
                print('Not found friend or friended, just skip...')
                continue
            user_friend = UserFriend(_id=user_friend_id, friend_id=friend_id, friended_id=friended_id,
                                     friend_display_name=friend.display_name, friend_email=friend.email, friend_profile_pic_url=friend.profile_pic_url,
                                     friended_display_name=friended.display_name, friended_email=friended.email, friended_profile_pic_url=friended.profile_pic_url, is_approved=is_approved)
            list_friends.append(user_friend)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_friends))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete user_friend migration after {} iteration with {} rows".format(count, total))

def migrate_poll_model():
    query = "SELECT id, title, user_id, created_date, updated_date from poll"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting poll migration...")   
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_polls = []
        for poll in res:
            (poll_id, title, user_id, created_date, updated_date) = poll
            poll_dsl = Poll(_id=poll_id, title=title, user_id=user_id, created_date=created_date, updated_date=updated_date)
            list_polls.append(poll_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_polls))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete poll migration after {} iteration with {} rows".format(count, total))


def migrate_user_model():
    query = "SELECT id, display_name, email, gender, age, reputation, first_name, middle_name, last_name  from user"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting user migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_users = []
        for user in res:
            (user_id, display_name, email, gender, age, reputation, first_name, middle_name, last_name) = user
            user_dsl = User(_id=user_id, display_name=display_name, email=email,
                gender=gender, age=age, reputation=reputation, first_name=first_name, middle_name=middle_name, last_name=last_name)
            list_users.append(user_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_users))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete user migration after {} iteration with {} rows".format(count, total))

def migrate_question_model():
    query = "SELECT id, question, title, user_id, slug, created_date, updated_date from question"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting question migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_questions = []
        for _question in res:
            (question_id, question, title, user_id, slug, created_date, updated_date) = _question
            question_dsl = Question(_id=question_id, question=strip_tags(question), title=title, user_id=user_id, slug=slug, created_date=created_date, updated_date=updated_date)
            list_questions.append(question_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_questions))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete question migration after {} iteration with {} rows".format(count, total))


def migrate_article_model():
    query = "SELECT id, html, title, user_id, slug, created_date, updated_date from article"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting article migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_articles = []
        for article in res:
            (article_id, html, title, user_id, slug, created_date, updated_date) = article
            article_dsl = Article(_id=article_id, html=strip_tags(html), title=title, user_id=user_id, slug=slug, created_date=created_date, updated_date=updated_date)
            list_articles.append(article_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_articles))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete article migration after {} iteration with {} rows".format(count, total))

def migrate_topic_model():
    query = "SELECT id, description, user_id, name, slug,is_fixed, created_date from topic"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting topic migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_topics = []
        for topic in res:
            (topic_id, description, user_id, name, slug,is_fixed, created_date) = topic
            topic_dsl = Topic(_id=topic_id, description=description, user_id=user_id, name=name, slug=slug, is_fixed=is_fixed, created_date=created_date)
            list_topics.append(topic_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_topics))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete topic migration after {} iteration with {} rows".format(count, total))

def migrate_post_model():
    query = "SELECT id, html, user_id, created_date, updated_date from post"
    limit = BATCH_SIZE
    offset = 0
    count = 0
    total = 0
    print("Starting post migration...")
    while True:
        res = select_with_pagination(query, limit=limit, offset=offset)
        if not res or len(res) == 0:
            break
        list_posts = []
        for post in res:
            (post_id, html, user_id, created_date, updated_date) = post
            post_dsl = Post(_id=post_id, html=strip_tags(html), user_id=user_id, created_date=created_date, updated_date=updated_date)
            list_posts.append(post_dsl)
        bulk(connections.get_connection(), (d.to_dict(True) for d in list_posts))
        print("Current iteration {} with length {}".format(count, len(res)))
        offset += limit
        count += 1
        total += len(res)
    print("Complete post migration after {} iteration with {} rows".format(count, total))

def main():
    for model_index in [user_index, question_index, post_index, article_index, topic_index, user_friend_index]:
        delete_index_if_exist(model_index)
    migrate_user_model()
    migrate_question_model()
    migrate_article_model()
    migrate_topic_model()
    migrate_post_model()
    migrate_poll_model()
    migrate_user_friend_model()

main()

def test():
    s = Question.search()
    q = Q("multi_match", query="n???i dung", fields=["question"])
    s = s.query(q)
    print(s.to_dict())
    response = s.execute()
    hits = response.hits
    for hit in hits:
        print(hit.to_dict())

test()
