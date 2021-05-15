#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func

# own modules
from common.cache import cache
from common.utils.types import UserRole
from app.modules.article.article_dto import ArticleDto
from app.modules.article.bookmark.bookmark_controller import ArticleBookmarkController
from app.constants import messages
from common.db import db
from common.dramatiq_producers import update_seen_articles
from common.controllers.controller import Controller
from common.models.vote import ArticleVote, VotingStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import is_sensitive
from common.es import get_model
from common.utils.util import strip_tags

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

        if not 'fixed_topic_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('fixed_topic_id'))

        # Handling user
        current_user = g.current_user  
        data['user_id'] = current_user.id

        # handling title
        data['title'] = data['title'].strip().capitalize()
        article = Article.query.filter(Article.title == data['title']).first()
        if article:
            return send_error(message=messages.ERR_ALREADY_EXISTS)

        if is_sensitive(data['title']):
            return send_error(message=messages.ERR_TITLE_INAPPROPRIATE)

        if  is_sensitive(data['html'], True):
            return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        article = self._parse_article(data=data, article=None)
        try:

            if article.scheduled_date is not None and article.scheduled_date < datetime.now():
                return send_error(message=messages.ERR_ARTICLE_SCHEDULED_BEFORE_CURRENT)

            if article.topics is not None:
                if len(article.topics) > 5:
                    return send_error(message=messages.ERR_TOPICS_MORE_THAN_5)

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
            
            vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
            if vote is not None:
                result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False

            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, ArticleDto.model_article_response))
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


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


    def get(self, args):

        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            current_user = g.current_user
            articles = res.get('data')

            results = []
            for article in articles:
                result = article.__dict__

                user = User.query.filter_by(id=article.user_id).first()
                result['user'] = user
                result['topics'] = article.topics
                result['fixed_topic'] = article.fixed_topic

                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                
                results.append(result)

            res['data'] = marshal(results, ArticleDto.model_article_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('Article', str(e)))

 
    def get_count(self, args):
        
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count}, message='Success')
        
        except Exception as e:
            print(e.__str__())
            return send_error(messages.ERR_NOT_LOAD_TOPICS)


    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('Article Id'))
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
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                update_seen_articles.send(article.id, current_user.id)
            
            return send_result(data=marshal(result, ArticleDto.model_article_response), message='Success')
        
        except Exception as e:
            print(e.__str__())
            pass
    
    def get_similar(self, args):
        if not 'title' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))
        
        title = args['title']
        if not 'fixed_topic_id' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('fixed_topic_id'))
        
        fixed_topic_id = args.get('fixed_topic_id')
        topic_ids = args.get('topic_id', None)

        if 'limit' in args:
            limit = int(args['limit'])
        else:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('limit'))
        
        try:
            current_user = g.current_user
            query = Article.query
            
            if args.get('exclude_article_id'):
                query = query.filter(Article.id != args.get('exclude_article_id'))
            
            title_similarity = db.func.SIMILARITY_STRING(Article.title, title).label('title_similarity')
            query = query.with_entities(Article, title_similarity).filter(title_similarity > 50)
            
            if fixed_topic_id is not None:
                query = query.filter(Article.fixed_topic_id == fixed_topic_id)
            
            if topic_ids is not None:
                query = query.filter(Article.topics.any(Topic.id.in_(topic_ids)))
            
            articles = query\
                .order_by(desc(title_similarity))\
                .limit(limit)\
                .all()

            results = list()
            for article in articles:
                article = article[0]

                result = article._asdict()
                result['user'] = article.user
                result['topics'] = article.topics

                if current_user:
                    
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False

                results.append(result)
        
            return send_result(data=marshal(results, ArticleDto.model_article_response), message='Success')
        
        except Exception as e:
            print(e.__str__())
            return send_error(message="Get similar articles failed. Error: "+ e.__str__())


    def update(self, object_id, data):
       
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('Article Id'))
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            article = Article.query.filter_by(id=object_id).first()
        else:
            article = Article.query.filter_by(slug=object_id).first()
        
        if article is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user
        if article.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        # Handling title
        if 'title' in data:
            data['title'] = data['title'].strip().capitalize()
            if is_sensitive(data['title']):
                return send_error(message=messages.ERR_TITLE_INAPPROPRIATE)

        # Handling html body
        if 'html' in data:
            if is_sensitive(data['html'], True):
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        article = self._parse_article(data=data, article=article)
        try:  
            if article.topics is not None and len(article.topics) > 5:
                return send_error(message=messages.ERR_TOPICS_MORE_THAN_5)

            article.updated_date = datetime.utcnow()
            article.last_activity = datetime.utcnow()
            article_dsl = ESArticle(_id=article.id)
            article_dsl.update(html=strip_tags(article.html), title=article.title, slug=article.slug, updated_date=article.updated_date)
            db.session.commit()
            cache.clear_cache(Article.__class__.__name__)

            result = article._asdict()
            result['user'] = article.user
            result['topics'] = article.topics

            vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()                    
            if vote is not None:
                result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False

            return send_result(message=messages.MSG_UPDATE_SUCCESS.format("Article"), data=marshal(result, ArticleDto.model_article_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format("Article", str(e)))

    def delete(self, object_id):
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
            return send_result(message=messages.MSG_DELETE_SUCCESS.format(object_id))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(object_id, str(e)))


    def update_slug(self):
        articles = Article.query.all()
        try:
            for article in articles:
                article.slug = slugify(article.title)
                db.session.commit()
            return send_result(marshal(articles, ArticleDto.model_article_response), message='Success')
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=e)


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
            
        if 'is_deleted' in data:
            try:
                article.is_deleted = bool(data['is_deleted'])
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


