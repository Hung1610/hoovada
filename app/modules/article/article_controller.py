#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import func

# own modules
from common.cache import cache
from common.utils.types import UserRole
from app.modules.article.article_dto import ArticleDto
from app.modules.article.bookmark.bookmark_controller import ArticleBookmarkController
from app.constants import messages
from common.db import db
from common.dramatiq_producers import update_seen_articles
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result
from common.es import get_model
from common.utils.util import strip_tags
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Article = db.get_model('Article')
ArticleShare = db.get_model('ArticleShare')
Topic = db.get_model('Topic')
TopicBookmark = db.get_model('TopicBookmark')
User = db.get_model('User')
UserFollow = db.get_model('UserFollow')
UserFriend = db.get_model('UserFriend')
ESArticle = get_model('Article')


class ArticleController(Controller):
    query_classname = 'Article'
    special_filtering_fields = ['from_date', 'to_date', 'title', 'topic_id', 'article_ids', 'draft']    
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count']

    def create(self, data):

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'title' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))

        if not 'html' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('html'))

        # default fixed_topic
        if 'fixed_topic_id' not in data:
            topic = Topic.query.filter(Topic.name == 'Nh???ng l??nh v???c kh??c', Topic.is_fixed == True).first()
            data['fixed_topic_id'] = topic.id

        # Handling user
        current_user = g.current_user  
        data['user_id'] = current_user.id

        # handling title
        data['title'] = data['title'].strip().capitalize()
        data = self.add_org_data(data)
        if data['entity_type'] == 'organization':
            data['is_draft'] = 1
        article = Article.query.filter(Article.title == data['title'], Article.is_draft == 0).first()
        if article:
            return send_error(message=messages.ERR_ALREADY_EXISTS)

        article = self._parse_article(data=data, article=None)
        try:

            if article.scheduled_date is not None and article.scheduled_date < datetime.utcnow():
                return send_error(message=messages.ERR_ARTICLE_SCHEDULED_BEFORE_CURRENT)

            db.session.add(article)
            db.session.flush()
            article_dsl = ESArticle(_id=article.id, html=strip_tags(article.html), title=article.title, user_id=article.user_id, slug=article.slug, created_date=article.created_date, updated_date=article.created_date)
            article_dsl.save()
            db.session.commit()
            cache.clear_cache(Article.__class__.__name__)

            update_seen_articles.send(article.id, current_user.id)
            controller = ArticleBookmarkController()
            controller.create(article_id=article.id)

            result = article._asdict()
            result['user'] = article.user
            if article.topics is not None:
                result['topics'] = article.topics
            
            result['is_upvoted_by_me'] = False
            result['is_downvoted_by_me'] = False
            result['is_bookmarked_by_me'] = True

            return send_result(data=marshal(result, ArticleDto.model_article_create_update_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):

        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            current_user = g.current_user
            articles = res.get('data')

            results = []
            for article in articles:
                result = article._asdict()

                user = User.query.filter_by(id=article.user_id).first()
                result['user'] = user
                result['topics'] = article.topics
                result['fixed_topic'] = article.fixed_topic                
                results.append(result)

            res['data'] = marshal(results, ArticleDto.model_article_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))

 
    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count})
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))

    def org_update_status(self, object_id, data):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
            
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            if object_id.isdigit():
                article = Article.query.filter_by(id=object_id).first()
            else:
                article = Article.query.filter_by(slug=object_id).first()
            
            if article is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            if article.organization is None or article.organization.user_id is None:
                return send_error(message=messages.ERR_ISSUE.format('Article must belong to an organization to perform this action'))
            if g.current_user and g.current_user.id != article.organization.user_id:
                return send_error(message=messages.ERR_NOT_AUTHORIZED)
            if not 'status' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('status'))
            if data['status'] == 'approved':
                article.is_draft = 0
                article.published_date = datetime.now()
            elif data['status'] == "drafted":
                article.is_draft = 1
                article.published_date = None
            else:
                return send_error(message=messages.ERR_ISSUE.format('status must be: approved or drafted'))
            db.session.commit()
            return send_result(data=marshal(article, ArticleDto.model_article_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    def get_by_id(self, object_id):
        
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:      
            if object_id.isdigit():
                article = Article.query.filter_by(id=object_id).first()
            else:
                article = Article.query.filter_by(slug=object_id).first()

            if article is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            article.views_count += 1
            db.session.commit()
            result = article._asdict()

            # get user info
            result['user'] = article.user
            result['fixed_topic'] = article.fixed_topic
            result['topics'] = article.topics

            current_user = g.current_user
            if current_user:
                update_seen_articles.send(article.id, current_user.id)
            
            return send_result(data=marshal(result, ArticleDto.model_article_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
    

    def get_similar(self, args):
        if not 'title' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))
        
        title = args['title']
        if not 'fixed_topic_id' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('fixed_topic_id'))
        
        fixed_topic_id = args.get('fixed_topic_id')
        topic_ids = args.get('topic_id', None)
        limit = 30
        if 'limit' in args:
            limit = int(args['limit'])
        try:
            current_user = g.current_user
            s = ESArticle.search()
            q = Q("multi_match", query=title, fields=["title", "html"])
            s = s.query(q)
            s = s[0:limit]
            response = s.execute()
            hits = response.hits
            results = list()
            for hit in hits:
                article_id = hit.meta.id
                article = Article.query.filter_by(id=article_id).first()
                if not article or article.title == title:
                    continue
                if fixed_topic_id and article.fixed_topic_id != fixed_topic_id:
                    continue
                if topic_ids and not article.topics:
                    continue
                if article.topics and topic_ids:
                    article_topic_ids = list(map(lambda x : x.id, article.topics))
                    intersected = all(item in topic_ids for item in article_topic_ids)
                    if not intersected:
                        continue
                if args.get('exclude_article_id') == article.id:
                    continue
                result = article._asdict()
                result['user'] = article.user
                result['topics'] = article.topics

                results.append(result)
            return send_result(data=marshal(results, ArticleDto.model_article_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))

    def _update_article_from_org(self, article, data):
        current_user = g.current_user
        if article.organization.user_id != current_user.id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        if 'is_draft' in data:
            return send_error(code=401, message=messages.ERR_NOT_ALLOWED_PARAMS.format('is_draft'))

        # Handling title
        if 'title' in data:
            data['title'] = data['title'].strip().capitalize()
            
        article = self._parse_article(data=data, article=article)
        try:  

            article.updated_date = datetime.utcnow()
            article.last_activity = datetime.utcnow()
            article_dsl = ESArticle(_id=article.id)
            article_dsl.update(html=strip_tags(article.html), title=article.title, slug=article.slug, updated_date=article.updated_date)
            db.session.commit()
            cache.clear_cache(Article.__class__.__name__)

            result = article._asdict()
            result['user'] = article.user
            result['topics'] = article.topics
            return send_result(data=marshal(result, ArticleDto.model_article_create_update_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def update(self, object_id, data):
       
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            article = Article.query.filter_by(id=object_id).first()
        else:
            article = Article.query.filter_by(slug=object_id).first()
        
        if article is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        
        if article.organization is not None and article.organization.user_id is not None:
            return self._update_article_from_org(article, data)

        current_user = g.current_user
        if article.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        # Handling title
        if 'title' in data:
            data['title'] = data['title'].strip().capitalize()
            
        article = self._parse_article(data=data, article=article)
        try:  

            article.updated_date = datetime.utcnow()
            article.last_activity = datetime.utcnow()
            article_dsl = ESArticle(_id=article.id)
            article_dsl.update(html=strip_tags(article.html), title=article.title, slug=article.slug, updated_date=article.updated_date)
            db.session.commit()
            cache.clear_cache(Article.__class__.__name__)

            result = article._asdict()
            result['user'] = article.user
            result['topics'] = article.topics
            return send_result(data=marshal(result, ArticleDto.model_article_create_update_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
            
        try:
            if object_id.isdigit():
                article = Article.query.filter_by(id=object_id).first()
            else:
                article = Article.query.filter_by(slug=object_id).first()

            if article is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if article.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
                
            db.session.delete(article)
            article_dsl = ESArticle(_id=article.id)
            article_dsl.delete()
            db.session.commit()
            cache.clear_cache(Article.__class__.__name__)
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_query(self):
        query = Article.query.join(User, isouter=True).filter(db.or_(Article.scheduled_date == None, datetime.utcnow() >= Article.scheduled_date))
        query = query.filter(db.or_(Article.user == None, User.is_deactivated != True))
        return query


    def apply_filtering(self, query, params):
        try:  
            query = super().apply_filtering(query, params)
            
            current_user = g.current_user
            if current_user:
                if not current_user.show_nsfw:
                    query = query.filter(Article.fixed_topic.has(db.func.coalesce(Topic.is_nsfw, False) == False))\
                        .filter(db.or_(db.not_(Article.topics.any()), Article.topics.any(Topic.is_nsfw == False)))
            
            if params.get('user_id'):
                get_my_own = False
                if g.current_user:
                    if params.get('user_id') == str(g.current_user.id):
                        get_my_own = True

                if not get_my_own:
                    query = query.filter(db.func.coalesce(Article.is_anonymous, False) != True)
            
            if params.get('title'):
                query = query.filter(Article.title.like(params.get('title')))
            
            if params.get('from_date'):
                query = query.filter(Article.created_date >= dateutil.parser.isoparse(params.get('from_date')))
            
            if params.get('to_date'):
                query = query.filter(Article.created_date <= dateutil.parser.isoparse(params.get('to_date')))
            
            if params.get('topic_id'):
                query = query.filter(Article.topics.any(Topic.id.in_(params.get('topic_id'))))

            if params.get('article_ids'):
                query = query.filter(Article.id.in_(params.get('article_ids')))
            
            if params.get('draft') is not None:
                if params.get('draft'):
                    query = query.filter(Article.is_draft == True)
                else:
                    query = query.filter(Article.is_draft != True)
            return query
        except Exception as e:
            print(e.__str__())
            raise e


    def _parse_article(self, data, article=None):
        
        if article is None:
            article = Article()
        
        if 'title' in data:
            try:
                article.title = data['title']
            except Exception as e:
                print(e.__str__())
                pass

        if 'html' in data:
            try:
                article.html = data['html']
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'user_id' in data:
            try:
                article.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'fixed_topic_id' in data:
            try:
                article.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'scheduled_date' in data:
            try:
                article.scheduled_date = dateutil.parser.isoparse(data.get('scheduled_date'))
            except Exception as e:
                print(e.__str__())
                pass
            
        if 'is_draft' in data:
            try:
                article.is_draft = bool(data['is_draft'])
            except Exception as e:
                print(e.__str__())
                pass
            
        if 'topic_ids' in data:
            topic_ids = data['topic_ids']
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e.__str__())
                    pass
            article.topics = topics

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    article.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    print(e.__str__())
                    pass

        return article


