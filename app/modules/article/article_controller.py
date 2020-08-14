#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal
from sqlalchemy import desc

# own modules
from app import db
from app.modules.article import constants
from app.modules.article.article import Article
from app.modules.article.article_dto import ArticleDto
from app.modules.article.voting.vote import ArticleVote, VotingStatusEnum
from app.modules.auth.auth_controller import AuthController
from app.modules.common.controller import Controller
from app.modules.topic.topic import Topic
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleController(Controller):
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
                is_sensitive = check_sensitive(article.html)
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
        # Get search parameters
        title, user_id, fixed_topic_id, created_date, updated_date, from_date, to_date, anonymous, topic_id = None, None, None, None, None, None, None, None, None
        if 'title' in args:
            title = args['title']
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e)
                pass
        if 'fixed_topic_id' in args:
            try:
                fixed_topic_id = int(args['fixed_topic_id'])
            except Exception as e:
                print(e)
                pass
        if 'created_date' in args:
            try:
                created_date = datetime.fromisoformat(args['created_date'])
            except Exception as e:
                print(e)
                pass
        if 'updated_date' in args:
            try:
                updated_date = datetime.fromisoformat(args['updated_date'])
            except Exception as e:
                print(e)
                pass
        if 'from_date' in args:
            try:
                from_date = datetime.fromisoformat(args['from_date'])
            except Exception as e:
                print(e)
                pass
        if 'to_date' in args:
            try:
                to_date = datetime.fromisoformat(args['to_date'])
            except Exception as e:
                print(e)
                pass
        if 'anonymous' in args:
            try:
                anonymous = int(args['anonymous'])
            except Exception as e:
                print(e)
                pass
        if 'topic_id' in args:
            try:
                topic_id = int(args['topic_id'])
            except Exception as e:
                print(e)
                pass

        query = Article.query  # query search from view
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
        if topic_id:
            query = query.filter(Article.topics.any(id=topic_id))

        articles = query.all()
        if articles and len(articles) > 0:
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
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                results.append(result)
            return send_result(marshal(results, ArticleDto.model_article_response), message='Success')
        else:
            return send_error(message=constants.msg_search_failed)

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        article = Article.query.filter_by(id=object_id).first()
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
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            except Exception as e:
                print(e)
                pass
            return send_result(data=marshal(result, ArticleDto.model_article_response), message='Success')

    def update(self, object_id, data, is_put=False):
        if object_id is None:
            return send_error(message=constants.msg_lacking_id)
        if not isinstance(data, dict):
            return send_error(message=constants.msg_wrong_data_format)

        article = Article.query.filter_by(id=object_id).first()
        if article is None:
            return send_error(message=constants.msg_not_found_with_id.format(object_id))
        if is_put:
            article.title, article.fixed_topic_id, article.html, article.user_hidden = None, None, None, None

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
            article, _ = self._parse_article(data=data, article=article)
            # check sensitive before updating
            is_sensitive = check_sensitive(article.title)
            if is_sensitive:
                return send_error(message=constants.msg_update_failed_insensitive_title)
            is_sensitive = check_sensitive(article.html)
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
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
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
            article = Article.query.filter_by(id=object_id).first()
            if article is None:
                return send_error(message=constants.msg_not_found_with_id.format(object_id))
            else:
                db.session.delete(article)
                db.session.commit()
                return send_result(message=constants.msg_delete_success_with_id.format(object_id))
        except Exception as e:
            print(e)
            return send_error(message=constants.msg_delete_failed_with_id.format(object_id))

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
            
        if 'is_deleted' in data:
            try:
                article.is_deleted = int(data['is_deleted'])
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
