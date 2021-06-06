#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import dateutil.parser
from flask_restx import marshal
from elasticsearch_dsl import Q

# own modules
from app.constants import messages
from common.db import db
from app.modules.search.search_dto import SearchDto
from common.models import Article, Question, Topic, User, UserBan, Post, Poll, UserFriend
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
                users.append(user._asdict())
                
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
                articles.append(article._asdict())
        return articles


    def _search_topic(self, args):
        start_from = 0
        size = 10
        
        if args['from'] is not None:
            start_from = int(args['from'])
        
        if args['size']:
            size = int(args['size'])
        
        is_fixed = None
        if 'is_fixed' in args:
            is_fixed = int(args['is_fixed'])

        s = ESTopic.search()
        q = Q("multi_match", query=args['value'], fields=["name"])
        s = s.query(q)
        s = s[start_from:size + 1]
        response = s.execute()
        hits = response.hits
        topics = []
        for h in hits:
            topic = db.session.query(Topic).filter_by(id=h.meta.id).first()

            if topic is not None:
                if (is_fixed in [0,1] and topic.is_fixed == is_fixed) or is_fixed is None:
                    topics.append(topic._asdict())
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
                questions.append(question._asdict())
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
            post = db.session.query(Post).filter_by(id=h.meta.id).first()
            if post is not None:
                result = post._asdict()
                result['highlighted_html'] = list(h.meta.highlight.html)
                posts.append(result)
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
            poll = db.session.query(Poll).filter_by(id=h.meta.id).first()
            if poll is not None:
                polls.append(poll._asdict())
        return polls
    
    def _search_user_friend(self, args, user_id):
        start_from = 0
        size = 10
        if args['from'] is not None:
            start_from = int(args['from'])
        if args['size']:
            size = int(args['size'])
        s = ESUserFriend.search()
        q = Q("multi_match", query=args['value'], fields=["friend_display_name", "friend_email", "friended_display_name", "friended_email"])
        bool_q_content = {
            "bool":{
                "should":[{"term":{"friend_id": user_id}},{"term":{"friended_id": user_id}}],
                "must": {"term": {"is_approved": 1}}
            }
        }
        bool_q = Q(bool_q_content)
        s = s.query(bool_q & q)
        s = s[start_from:size + 1]
        response = s.execute()
        hits = response.hits
        users = []
        for h in hits:
            # must validate db's record before being sent to client
            user_friend = db.session.query(UserFriend).filter_by(id=h.meta.id).first()
            if user_friend is not None:
                users.append(user_friend._asdict())
        return users 

    def search(self, args):

        if 'value' not in args:
            return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

        valueSearch = args.get('value')
        search_args = {
            'value': valueSearch,
            'from': '0',
            'size': '10'
        }
        try:
            users = self._search_user(search_args, emailSearch=True)
            questions = self._search_question(search_args)
            topics = self._search_topic(search_args)
            articles = self._search_article(search_args)
            posts = self._search_post(valueSearch)
            polls = self._search_poll(search_args)
            data = {'question': questions, 'topic': topics, 'user': users, 'article': articles,'post': posts, 'polls': polls}

            return send_result(data=marshal(data, SearchDto.model_event_search_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))        


    def search_article_by_title(self, args):
        try:
            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            articles = self._search_article(search_args)
            return send_result(data=marshal(articles, SearchDto.model_search_article_res))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def search_user_by_name_or_email(self, args):
        try:
            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            users = self._search_user(search_args, emailSearch=True)
            return send_result(data=marshal(users, SearchDto.model_search_user_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))

    def search_poll_by_title(self, args):
        try:
            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            polls = self._search_poll(search_args)
            return send_result(data=marshal(polls, SearchDto.model_search_poll_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def search_question_by_title(self, args):
        try:
            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size')
            }
            questions = self._search_question(search_args)
            return send_result(data=marshal(questions, SearchDto.model_search_question_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def search_topic_by_name(self, args):
        try:
            if not isinstance(args, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            is_fixed  = None
            if 'is_fixed' in args and args['is_fixed'] is not None:
                is_fixed = int(args.get('is_fixed'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size'),
                'is_fixed': is_fixed,
            }

            topics = self._search_topic(search_args)
            return send_result(data=marshal(topics, SearchDto.model_search_topic_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
    

    def search_friend_by_name_or_email(self, args, user_id):
        try:
            if not args.get('value'):
                return send_result(data={}, message=messages.ERR_PLEASE_PROVIDE.format('value'))

            search_args = {
                'value': args.get('value'),
                'from': args.get('from'),
                'size': args.get('size'),
                'is_approved': args.get('is_approved')
            }
            user_friends = self._search_user_friend(search_args, user_id)
            return send_result(data=marshal(user_friends, SearchDto.model_search_user_friend_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
            
