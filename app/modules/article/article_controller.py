#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from slugify import slugify
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal
from sqlalchemy import desc, text, func
from bs4 import BeautifulSoup

# own modules
from app import db
from app.modules.article import constants
from app.modules.article.article import Article
from app.modules.article.article_dto import ArticleDto
from app.modules.article.voting.vote import ArticleVote, VotingStatusEnum
from app.modules.article.favorite.favorite import ArticleFavorite
from app.modules.auth.auth_controller import AuthController
from app.modules.common.controller import Controller
from app.modules.topic.topic import Topic
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive
from app.modules.topic.bookmark.bookmark import TopicBookmark

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleController(Controller):
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)
        if not 'title' in data:
            return send_error(message=constants.msg_must_contain_title)
        if not 'fixed_topic_id' in data:
            return send_error(message=constants.msg_must_contain_fixed_topic_id)
        if not 'topic_ids' in data:
            return send_error(message=constants.msg_must_contain_topics_id)

        current_user, _ = AuthController.get_logged_user(request)
        data['user_id'] = current_user.id
        try:
            is_sensitive = check_sensitive(data['title'])
            if is_sensitive:
                return send_error(message=constants.msg_insensitive_title)

            article = Article.query.filter(Article.title == data['title']).filter(Article.user_id == data['user_id']).first()
            if not article:  # the article does not exist
                article, topic_ids = self._parse_article(data=data, article=None)
                is_sensitive = check_sensitive(''.join(BeautifulSoup(article.html, "html.parser").stripped_strings))
                if is_sensitive:
                    return send_error(message=constants.msg_insensitive_body)
                article.created_date = datetime.utcnow()
                article.last_activity = datetime.utcnow()
                db.session.add(article)
                db.session.commit()
                # Add topics and get back list of topic for article
                try:
                    result = article.__dict__
                    # get user info
                    user = User.query.filter_by(id=article.user_id).first()
                    result['user'] = user
                    # add article_topics
                    topics = []
                    for topic_id in topic_ids:
                        try:
                            topic = Topic.query.filter_by(id=topic_id).first()
                            article.topics.append(topic)
                            db.session.commit()
                            topics.append(topic)
                        except Exception as e:
                            print(e)
                            pass
                    result['topics'] = topics
                    
                    # upvote/downvote status for current user
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                    return send_result(message=constants.msg_create_success,
                                       data=marshal(result, ArticleDto.model_article_response))
                except Exception as e:
                    print(e)
                    return send_result(data=marshal(article, ArticleDto.model_article_response),
                                       message=constants.msg_create_success_without_topics)
            else:  # topic already exist
                return send_error(message=constants.msg_article_already_exists.format(data['title']))
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=constants.msg_create_failed)

    def get(self, args):
        """
        Search articles.
        :param args:
        :return:
        """
        try:
            # Get search parameters
            title, user_id, fixed_topic_id, created_date, updated_date, from_date, to_date, topic_ids, draft, is_deleted = None, None, None, None, None, None, None, None, None, None
            if args.get('title'):
                title = args['title']
            if args.get('user_id'):
                try:
                    user_id = int(args['user_id'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('fixed_topic_id'):
                try:
                    fixed_topic_id = int(args['fixed_topic_id'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('created_date'):
                try:
                    created_date = dateutil.parser.isoparse(args['created_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('updated_date'):
                try:
                    updated_date = dateutil.parser.isoparse(args['updated_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('from_date'):
                try:
                    from_date = dateutil.parser.isoparse(args['from_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('to_date'):
                try:
                    to_date = dateutil.parser.isoparse(args['to_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('topic_id'):
                try:
                    topic_ids = args['topic_id']
                except Exception as e:
                    print(e)
                    pass
            if args.get('draft'):
                try:
                    draft = bool(args['draft'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('is_deleted'):
                try:
                    is_deleted = bool(args['is_deleted'])
                except Exception as e:
                    print(e)
                    pass

            query = Article.query.filter(db.or_(Article.scheduled_date == None, datetime.utcnow() >= Article.scheduled_date))
            query = query.filter(Article.article_by_user.is_deactivated != True)
            if not is_deleted:
                query = query.filter(Article.is_deleted != True)
            if title and not str(title).strip().__eq__(''):
                title = '%' + title.strip() + '%'
                query = query.filter(Article.title.like(title))
            if user_id:
                query = query.filter(Article.user_id == user_id)
            if fixed_topic_id:
                query = query.filter(Article.fixed_topic_id == fixed_topic_id)
            if created_date:
                query = query.filter(Article.created_date == created_date)
            if updated_date:
                query = query.filter(Article.updated_date == updated_date)
            if from_date:
                query = query.filter(Article.created_date >= from_date)
            if to_date:
                query = query.filter(Article.created_date <= to_date)
            if topic_ids:
                query = query.filter(Article.topics.any(Topic.id.in_(topic_ids)))
            if draft is not None:
                if draft:
                    query = query.filter(Article.is_draft == True)
                else:
                    query = query.filter(Article.is_draft != True)

            ordering_fields_desc = args.get('order_by_desc')
            if ordering_fields_desc:
                for ordering_field in ordering_fields_desc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Article, ordering_field)
                        query = query.order_by(db.desc(column_to_sort))

            ordering_fields_asc = args.get('order_by_asc')
            if ordering_fields_asc:
                for ordering_field in ordering_fields_asc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Article, ordering_field)
                        query = query.order_by(db.asc(column_to_sort))
                        
            articles = query.all()
            results = []
            for article in articles:
                result = article.__dict__
                # get user info
                user = User.query.filter_by(id=article.user_id).first()
                result['user'] = user
                # get all topics that article belongs to
                result['topics'] = article.topics
                # get fixed topic name
                result['fixed_topic_name'] = article.fixed_topic.name
                # get current user voting status for this article
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            return send_result(marshal(results, ArticleDto.model_article_response), message='Success')
        except Exception as e:
            return send_error(message=constants.msg_search_failed)

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        if object_id.isdigit():
            article = Article.query.filter_by(id=object_id).first()
        else:
            article = Article.query.filter_by(slug=object_id).first()
        if article is None:
            return send_error(message=constants.msg_not_found_with_id.format(object_id))
        else:
            article.views_count += 1
            db.session.commit()
            result = article.__dict__
            # get user info
            result['user'] = article.article_by_user
            # get all topics that article belongs to
            result['topics'] = article.topics
            # upvote/downvote status
            try:
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
            except Exception as e:
                print(e)
                pass
            return send_result(data=marshal(result, ArticleDto.model_article_response), message='Success')
    
    def get_similar(self, args):
        if not 'title' in args:
            return send_error(message='Please provide at least the title.')
        title = args['title']
        if not 'fixed_topic_id' in args:
            return send_error(message='Please provide the fixed_topic_id.')
        fixed_topic_id = args.get('fixed_topic_id')
        if not 'topic_id' in args:
            return send_error(message='Please provide the topic_id.')
        topic_ids = args.get('topic_id')
        if 'limit' in args:
            limit = int(args['limit'])
        else:
            return send_error(message='Please provide limit')
        
        try:
            current_user, _ = AuthController.get_logged_user(request)
            query = Article.query
            title_similarity = db.func.SIMILARITY_STRING(title, Article.title).label('title_similarity')
            query = query.with_entities(Article, title_similarity)\
                .filter(title_similarity > 50)
            if fixed_topic_id:
                query = query.filter(Article.fixed_topic_id == fixed_topic_id)
            if topic_ids:
                query = query.filter(Article.topics.any(Topic.id.in_(topic_ids)))
            articles = query\
                .order_by(desc(title_similarity))\
                .limit(limit)\
                .all()
            results = list()
            for article in articles:
                article = article[0]
                result = article._asdict()
                # get user info
                result['user'] = article.article_by_user
                result['topics'] = article.topics
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            return send_result(data=marshal(results, ArticleDto.model_article_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get similar articles failed. Error: "+ e.__str__())

    def update(self, object_id, data, is_put=False):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)

        if object_id.isdigit():
            article = Article.query.filter_by(id=object_id).first()
        else:
            article = Article.query.filter_by(slug=object_id).first()
        if article is None:
            return send_error(message=constants.msg_not_found_with_id.format(object_id))
        if is_put:
            db.session.delete(article)
            return self.create(data)
        article, _ = self._parse_article(data=data, article=article)

        if 'topic_ids' in data:
            topic_ids = data['topic_ids']
            # update article topics
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            article.topics = topics
        try:
            # check sensitive before updating
            is_sensitive = check_sensitive(article.title)
            if is_sensitive:
                return send_error(message=constants.msg_update_failed_insensitive_title)
            is_sensitive = check_sensitive(''.join(BeautifulSoup(article.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=constants.msg_update_failed_insensitive_body)
            # update topics to article_topic table
            article.updated_date = datetime.utcnow()
            article.last_activity = datetime.utcnow()
            db.session.commit()
            
            result = article.__dict__
            # get user info
            result['user'] = article.article_by_user
            # get all topics that article belongs to
            result['topics'] = article.topics
            # upvote/downvote status
            try:
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
            except Exception as e:
                print(e)
                pass
            return send_result(message=constants.msg_update_success,
                                data=marshal(result, ArticleDto.model_article_response))
        except Exception as e:
            print(e)
            return send_error(message=constants.msg_update_failed)

    def delete(self, object_id):
        try:
            if object_id.isdigit():
                article = Article.query.filter_by(id=object_id).first()
            else:
                article = Article.query.filter_by(slug=object_id).first()
            if article is None:
                return send_error(message=constants.msg_not_found_with_id.format(object_id))
            else:
                db.session.delete(article)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(object_id))
        except Exception as e:
            print(e)
            return send_error(message=constants.msg_delete_failed_with_id.format(object_id))

    def update_slug(self):
        articles = Article.query.all()
        try:
            for article in articles:
                article.slug = slugify(article.title)
                db.session.commit()
            return send_result(marshal(articles, ArticleDto.model_article_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

    def _parse_article(self, data, article=None):
        if article is None:
            article = Article()
        if 'title' in data:
            try:
                article.title = data['title']
            except Exception as e:
                print(e)
                pass
        if 'user_id' in data:
            try:
                article.user_id = data['user_id']
            except Exception as e:
                print(e)
                pass
        if 'fixed_topic_id' in data:
            try:
                article.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e)
                pass
        if 'html' in data:
            article.html = data['html']
        if 'user_hidden' in data:
            try:
                article.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                article.user_hidden = False
                print(e)
                pass

        if 'scheduled_date' in data:
            try:
                article.scheduled_date = data['scheduled_date']
            except Exception as e:
                print(e)
                pass
            
        if 'is_draft' in data:
            try:
                article.is_draft = bool(data['is_draft'])
            except Exception as e:
                print(e)
                pass
            
        if 'is_deleted' in data:
            try:
                article.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                print(e)
                pass

        topic_ids = None
        if 'topic_ids' in data:
            try:
                topic_ids = data['topic_ids']
            except Exception as e:
                print(e)
                pass
        return article, topic_ids

    def get_user_hot(self,page=1):
        page_size = 20
        articles = None
        if page > 0 :
            page = page - 1
            query = db.session.query(Article).order_by(desc(text("upvote_count + downvote_count + share_count + favorite_count")),desc(Article.created_date))
            # get current user voting status for this article
            current_user, _ = AuthController.get_logged_user(request)
            if current_user:
               query = db.session.query(Article).outerjoin(TopicBookmark,TopicBookmark.id==Article.fixed_topic_id).order_by(desc(func.field(TopicBookmark.user_id, current_user.id)),desc(text("upvote_count + downvote_count + share_count + favorite_count")),desc(Article.created_date))
            else:
                query = db.session.query(Article).order_by(desc(text("upvote_count + downvote_count + share_count + favorite_count")),desc(Article.created_date))

            articles = query.offset(page * page_size).limit(page_size).all()

        if articles is not None and len(articles) > 0:
            return send_result(data=marshal(articles, ArticleDto.model_article_response), message='Success')
        else:
            return send_result(message='Could not find any articles')

