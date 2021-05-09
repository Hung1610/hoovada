#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import ast
import re
from datetime import datetime
import dateutil.parser
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter, Index, Q

# third-party modules
from flask_restx import marshal
from sqlalchemy import or_

# own modules
from common.db import db
from app.modules.search.search_dto import SearchDto
from common.models import Article, Question, Topic, User, UserBan, Post
from common.utils.response import send_error, send_result
from common.es import get_model

ESUser = get_model("User")
ESArticle = get_model("Article")
ESTopic = get_model("Topic")
ESQuestion = get_model("Question")
ESPost = get_model("Post")

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

extensionsToCheck = ('ạ','ả','ã','à','á','â','ậ','ầ','ấ','ẩ','ẫ','ă','ắ','ằ','ặ','ẳ','ẵ','ó','ò','ọ','õ','ỏ','ô','ộ','ổ','ỗ','ồ','ố','ơ','ờ','ớ','ợ','ở','ỡ','é','è','ẻ','ẹ','ẽ','ê','ế','ề','ệ','ể','ễ','ú','ù','ụ','ủ','ũ','ư','ự','ữ','ử','ừ','ứ','í','ì','ị','ỉ','ĩ','ý','ỳ','ỷ','ỵ','ỹ','đ')

class SearchController():

    def _search_user(self, valueSearch):
        s = ESUser.search()
        q = Q("multi_match", query=valueSearch, fields=["display_name", "email", "first_name", "last_name", "middle_name"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        users = []
        for h in hits:
            user = db.session.query(User).filter_by(id=h.meta.id).first()
            user_ban = db.session.query(UserBan).filter_by(user_id=h.meta.id).first()
            if user is not None and user.is_private != 1 and user.is_deactivated != 1 and user_ban is None:
                users.append({
                    "id": h.meta.id,
                    "display_name": h.display_name,
                    "email": h.email
                })
        return users

    def _search_article(self, valueSearch):
        s = ESArticle.search()
        q = Q("multi_match", query=valueSearch, fields=["title", "html"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        articles = []
        for h in hits:
            article = db.session.query(Article).filter_by(id=h.meta.id).first()
            if article is not None and article.is_deleted != 1 and article.is_draft != 1:
                articles.append({
                    "id": h.meta.id,
                    "slug": h.slug,
                    "title": h.title
                })
        return articles

    def _search_topic(self, valueSearch):
        s = ESTopic.search()
        q = Q("multi_match", query=valueSearch, fields=["name"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        topics = []
        for h in hits:
            topics.append({
                "id": h.meta.id,
                "slug": h.slug,
                "name": h.name
            })
        return topics

    def _search_question(self, valueSearch):
        s = ESQuestion.search()
        q = Q("multi_match", query=valueSearch, fields=["title", "question"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        questions = []
        for h in hits:
            question = db.session.query(Question).filter_by(id=h.meta.id).first()
            if question is not None and question.is_deleted != 1 and question.is_private != 1:
                questions.append({
                    "id": h.meta.id,
                    "slug": h.slug,
                    "title": h.title
                })
        return questions
    
    def _search_post(self, valueSearch):
        s = ESPost.search()
        q = Q("multi_match", query=valueSearch, fields=["html"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        posts = []
        for h in hits:
            posts.append({
                "id": h.meta.id,
                "html": h.html,
            })
        return posts

    def search_elastic(self, args):
        """ Search data from elastic search server.
        """
        valueSearch = args.get('value')
        
        if not valueSearch:
            return send_result(data={}, message='Search value not provided')
                
        if any(ext in valueSearch for ext in extensionsToCheck) == True:
            emailSearch = True
        else:
            emailSearch = False
        users = self._search_user(valueSearch)
        questions = self._search_question(valueSearch)
        topics = self._search_topic(valueSearch)
        articles = self._search_article(valueSearch)
        posts = self._search_post(valueSearch)
        data = {'question': questions, 'topic': topics, 'user': users, 'article': articles,'post': posts}
        return send_result(data, message='Success')

    def search(self, args):
        """ Search questions.
        """
        self.search_elastic(args)
        valueSearch = args.get('value')
        
        if not valueSearch:
            return send_result(data={}, message='Search value not provided')
                
        if any(ext in valueSearch for ext in extensionsToCheck) == True:
            emailSearch = True
        else:
            emailSearch = False
        
        queryQuestion = db.session.query(Question)  # query search from view question
        queryTopic = db.session.query(Topic)  # query search from view topic
        queryUser = db.session.query(User)  # query search from view user
        queryArticle = db.session.query(Article)  # query search from view user

        valueSearch = '%' + valueSearch.strip() + '%'
        queryQuestion = queryQuestion.filter(Question.title.like(valueSearch))
        queryTopic = queryTopic.filter(Topic.name.like(valueSearch))
        queryArticle = queryArticle.filter(Article.title.like(valueSearch))

        if emailSearch == False:
            queryUser = queryUser.filter(or_(User.email.like(valueSearch), User.display_name.like(valueSearch))).filter(User.is_deactivated == False, User.is_private == False)
        else:
            queryUser = queryUser.filter(User.display_name.like(valueSearch)).filter(User.is_deactivated == False, User.is_private == False)
        
        questions = queryQuestion.all()
        topics = queryTopic.all()
        users = queryUser.all()
        articles = queryArticle.all()

        resultQuestions = list()
        resultTopics = list()
        resultUsers = list()
        resultArticles = list()

        # search questions
        if questions is not None and len(questions) > 0:
            resultQuestions = marshal(questions, SearchDto.model_search_question_res)

        # search topics
        if topics is not None and len(topics) > 0:
            resultTopics = marshal(topics, SearchDto.model_search_topic_res)

        # search users
        if users is not None and len(users) > 0:
            resultUsers = marshal(users, SearchDto.model_search_user_res)

        # search articles
        if articles is not None and len(articles) > 0:
            resultArticles = marshal(articles, SearchDto.model_search_article_res)

        data = {'question': resultQuestions, 'topic': resultTopics, 'user': resultUsers, 'article': resultArticles}
        return send_result(data, message='Success')