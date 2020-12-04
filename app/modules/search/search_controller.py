#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implement logic for search APIs"""

import ast
# built-in modules
import re
from datetime import datetime

import dateutil.parser
from flask_restx import marshal
# third-party modules
from sqlalchemy import or_

from common.models.model import db
from app.modules.search.search_dto import SearchDto
# own modules
from common.models import Article, Question, Topic, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

extensionsToCheck = ('ạ','ả','ã','à','á','â','ậ','ầ','ấ','ẩ','ẫ','ă','ắ','ằ','ặ','ẳ','ẵ','ó','ò','ọ','õ','ỏ','ô','ộ','ổ','ỗ','ồ','ố','ơ','ờ','ớ','ợ','ở','ỡ','é','è','ẻ','ẹ','ẽ','ê','ế','ề','ệ','ể','ễ','ú','ù','ụ','ủ','ũ','ư','ự','ữ','ử','ừ','ứ','í','ì','ị','ỉ','ĩ','ý','ỳ','ỷ','ỵ','ỹ','đ')

class SearchController():

    def search(self, args):
        """ Search questions.
        """
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
            queryUser = queryUser.filter(or_(User.email.like(valueSearch), User.display_name.like(valueSearch)))
        else:
            queryUser = queryUser.filter(User.display_name.like(valueSearch))
        
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