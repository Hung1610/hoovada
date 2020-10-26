#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implement logic for search APIs"""

# built-in modules
import re
import ast
from datetime import datetime

# third-party modules
from sqlalchemy import or_
from flask_restx import marshal
import dateutil.parser

# own modules
from app.modules.article.article import Article
from common.models.question import Question
from app.modules.topic.topic import Topic
from app.modules.user.user import User
from app.modules.search.search_dto import SearchDto
from common.utils.response import send_error, send_result
from app import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

extensionsToCheck = ('ạ','ả','ã','à','á','â','ậ','ầ','ấ','ẩ','ẫ','ă','ắ','ằ','ặ','ẳ','ẵ','ó','ò','ọ','õ','ỏ','ô','ộ','ổ','ỗ','ồ','ố','ơ','ờ','ớ','ợ','ở','ỡ','é','è','ẻ','ẹ','ẽ','ê','ế','ề','ệ','ể','ễ','ú','ù','ụ','ủ','ũ','ư','ự','ữ','ử','ừ','ứ','í','ì','ị','ỉ','ĩ','ý','ỳ','ỷ','ỵ','ỹ','đ')

class SearchController():

    def search(self, args):
        """ Search questions.
        """

        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        value = None
        if 'value' in args:
            try:
                valueSearch = args['value']
                
                if any(ext in valueSearch for ext in extensionsToCheck) == True:
                    emailSearch = True
                else:
                    emailSearch = False
            except Exception as e:
                print(e.__str__())
                pass
        
        queryQuestion = db.session.query(Question)  # query search from view question
        queryTopic = db.session.query(Topic)  # query search from view topic
        queryUser = db.session.query(User)  # query search from view user
        queryArticle = db.session.query(Article)  # query search from view user

        is_filter = False

        if valueSearch is not None and not str(valueSearch).strip().__eq__(''):
            valueSearch = '%' + valueSearch.strip() + '%'
            queryQuestion = queryQuestion.filter(Question.title.like(valueSearch))
            queryTopic = queryTopic.filter(Topic.name.like(valueSearch))
            queryArticle = queryArticle.filter(Article.title.like(valueSearch))

            if emailSearch == False:
                queryUser = queryUser.filter(or_(User.email.like(valueSearch), User.display_name.like(valueSearch)))
            else:
                queryUser = queryUser.filter(User.display_name.like(valueSearch))
            is_filter = True
        
        if is_filter:
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
                for question in questions:
                    result = question.__dict__
                    resultQuestions.append(result)

                resultQuestions = marshal(resultQuestions, SearchDto.model_search_question_res)

            # search topics
            if topics is not None and len(topics) > 0:
                for topic in topics:
                    result = topic.__dict__
                    resultTopics.append(result)

                resultTopics = marshal(resultTopics, SearchDto.model_search_topic_res)

            # search users
            if users is not None and len(users) > 0:
                for user in users:
                    result = user.__dict__
                    resultUsers.append(result)

                resultUsers = marshal(resultUsers, SearchDto.model_search_user_res)

            # search articles
            if articles is not None and len(users) > 0:
                for article in articles:
                    result = article.__dict__
                    resultArticles.append(result)

                resultArticles = marshal(resultArticles, SearchDto.model_search_article_res)
            
            if resultQuestions == [] and resultTopics == [] and resultUsers == [] and resultArticles == []:
                return send_result(message='Could not find any result')

            data = {'question': resultQuestions, 'topic': resultTopics, 'user': resultUsers, 'article': resultArticles}
            return send_result(data, message='Success')
        else:
            return send_error(message='Could not find data. Please check your parameters again.')