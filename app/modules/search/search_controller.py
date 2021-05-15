#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import ast
import re
from datetime import datetime

# third-party modules
import dateutil.parser
from flask_restx import marshal
from sqlalchemy import or_
from elasticsearch_dsl import Q

# own modules
from common.db import db
from app.modules.search.search_dto import SearchDto
from common.models import Article, Question, Topic, User, UserBan, Post, Poll
from common.utils.response import send_error, send_result
from common.es import get_model


ESUser = get_model("User")
ESArticle = get_model("Article")
ESTopic = get_model("Topic")
ESQuestion = get_model("Question")
ESPost = get_model("Post")
ESPoll = get_model("Poll")
ESUserFriend = get_model('UserFriend')

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

extensionsToCheck = ('ạ','ả','ã','à','á','â','ậ','ầ','ấ','ẩ','ẫ','ă','ắ','ằ','ặ','ẳ','ẵ','ó','ò','ọ','õ','ỏ','ô','ộ','ổ','ỗ','ồ','ố','ơ','ờ','ớ','ợ','ở','ỡ','é','è','ẻ','ẹ','ẽ','ê','ế','ề','ệ','ể','ễ','ú','ù','ụ','ủ','ũ','ư','ự','ữ','ử','ừ','ứ','í','ì','ị','ỉ','ĩ','ý','ỳ','ỷ','ỵ','ỹ','đ')

class SearchController():

    def _search_user(self, args, emailSearch):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        fields = ["display_name", "first_name", "last_name", "middle_name"]
        if emailSearch is True:
            fields.append("email")
        s = ESUser.search()
        q = Q("multi_match", query=args['value'], fields=fields)
        s = s.query(q)
        s = s[start_from:size + 1]
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

    def _search_article(self, args):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        s = ESArticle.search()
        q = Q("multi_match", query=args['value'], fields=["title"])
        s = s.query(q)
        s = s[start_from:size + 1]
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

    def _search_topic(self, args):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        s = ESTopic.search()
        q = Q("multi_match", query=args['value'], fields=["name"])
        s = s.query(q)
        s = s[start_from:size + 1]
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

    def _search_question(self, args):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        s = ESQuestion.search()
        q = Q("multi_match", query=args['value'], fields=["title"])
        s = s.query(q)
        s = s[start_from:size + 1]
        response = s.execute()
        hits = response.hits
        questions = []
        for h in hits:
            question = db.session.query(Question).filter_by(id=h.meta.id).first()
            if question is not None and question.is_deleted != 1 and question.is_private != 1:
                questions.append({
                    "id": h.meta.id,
                    "slug": h.slug,
                    "question": question.question,
                    "title": h.title
                })
        return questions
    
    def _search_post(self, valueSearch):
        s = ESPost.search()
        s = s.highlight("html", fragment_size=100)
        q = Q("multi_match", query=valueSearch, fields=["html"])
        s = s.query(q)
        response = s.execute()
        hits = response.hits
        posts = []
        for h in hits:
            posts.append({
                "id": h.meta.id,
                "highlighted_html": list(h.meta.highlight.html),
            })
        return posts
    
    def _search_poll(self, args):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        s = ESPoll.search()
        q = Q("multi_match", query=args['value'], fields=["title"])
        s = s.query(q)
        s = s[start_from:size + 1]
        response = s.execute()
        hits = response.hits
        polls = []
        for h in hits:
            polls.append({
                "id": h.meta.id,
                "title": h.title
            })
        return polls
    
    def _search_user_friend(self, args, user_id):
        start_from = 0
        size = 10
        is_approved = 1
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        if args['is_approved']:
            is_approved = int(args['is_approved'])
        s = ESUserFriend.search()
        q = Q("multi_match", query=args['value'], fields=["friend_display_name", "friend_email", "friended_display_name", "friended_email"])
        bool_q_content = {
            "bool":{
                "should":[{"term":{"friend_id": user_id}},{"term":{"friended_id": user_id}}],
                "must": {"term": {"is_approved": is_approved}}
            }
        }
        bool_q = Q(bool_q_content)
        s = s.query(bool_q & q)
        s = s[start_from:size + 1]
        response = s.execute()
        hits = response.hits
        users = []
        for h in hits:
            print(h)
            users.append({
                "id": h.meta.id,
                "friend_id": h.friend_id,
                "friend_display_name": h.friend_display_name,
                "friend_email": h.friend_email,
                "friend_profile_pic_url": h.friend_profile_pic_url,
                "friended_id": h.friended_id,
                "friended_display_name": h.friended_display_name,
                "friended_email": h.friended_email,
                "friended_profile_pic_url": h.friended_profile_pic_url,
                "is_approved": h.is_approved
            })
        return users 

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
        search_args = {
            'value': valueSearch,
            'from': '0',
            'size': '10'
        }
        users = self._search_user(search_args, emailSearch)
        questions = self._search_question(search_args)
        topics = self._search_topic(search_args)
        articles = self._search_article(search_args)
        posts = self._search_post(valueSearch)
        polls = self._search_poll(search_args)
        data = {'question': questions, 'topic': topics, 'user': users, 'article': articles,'post': posts, 'polls': polls}
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
            resultQuestions = marshal(questions, SearchDto.model_search_question_response)

        # search topics
        if topics is not None and len(topics) > 0:
            resultTopics = marshal(topics, SearchDto.model_search_topic_response)

        # search users
        if users is not None and len(users) > 0:
            resultUsers = marshal(users, SearchDto.model_search_user_response)

        # search articles
        if articles is not None and len(articles) > 0:
            resultArticles = marshal(articles, SearchDto.model_search_article_res)

        data = {'question': resultQuestions, 'topic': resultTopics, 'user': resultUsers, 'article': resultArticles}
        return send_result(data, message='Success')

    def search_article_by_title(self, args):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the title to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            articles = self._search_article(search_args)
            return send_result(data=marshal(articles, SearchDto.model_search_article_res), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load articles. Contact your administrator for solution.")

    def search_user_by_name_or_email(self, args):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the display name or email to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            users = self._search_user(search_args, emailSearch=True)
            return send_result(data=marshal(users, SearchDto.model_search_user_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load users. Contact your administrator for solution.")

    def search_poll_by_title(self, args):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the title to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            polls = self._search_poll(search_args)
            return send_result(data=marshal(polls, SearchDto.model_search_poll_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load polls. Contact your administrator for solution.")

    def search_question_by_title(self, args):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the title to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            questions = self._search_question(search_args)
            return send_result(data=marshal(questions, SearchDto.model_search_question_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load questions. Contact your administrator for solution.")

    def search_topic_by_name(self, args):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the title to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            topics = self._search_topic(search_args)
            return send_result(data=marshal(topics, SearchDto.model_search_topic_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load topics. Contact your administrator for solution.")
    
    def search_friend_by_name_or_email(self, args, user_id):
        try:
            if not args.get('value'):
                return send_error(message='Please provide the title to search.')
            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size'),
                'is_approved': args.get('is_approved')
            }
            user_friends = self._search_user_friend(search_args, user_id)
            return send_result(data=marshal(user_friends, SearchDto.model_search_user_friend_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load topics. Contact your administrator for solution.")   
            
