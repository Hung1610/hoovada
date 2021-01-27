#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from logging import log
import re
from datetime import datetime

# third-party modules
import dateutil.parser
from bs4 import BeautifulSoup
from flask import current_app, g, request
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func, text

# own modules
from app.modules.article import constants
from app.modules.article.article_dto import ArticleDto
from app.constants import messages
from common.utils.checker import check_spelling
from common.db import db
from common.dramatiq_producers import new_article_notify_user_list, update_seen_articles
from common.controllers.controller import Controller
from common.models.vote import ArticleVote, VotingStatusEnum
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Article = db.get_model('Article')
ArticleFavorite = db.get_model('ArticleFavorite')
ArticleShare = db.get_model('ArticleShare')
Topic = db.get_model('Topic')
TopicBookmark = db.get_model('TopicBookmark')
User = db.get_model('User')
UserFollow = db.get_model('UserFollow')
UserFriend = db.get_model('UserFriend')


class ArticleController(Controller):
    query_classname = 'Article'
    special_filtering_fields = ['from_date', 'to_date', 'draft', 'topic_id', 'title', 'is_created_by_friend', 'hot']
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count']

    def create(self, data):
        try:
            if not isinstance(data, dict):
                return send_error(message=constants.msg_wrong_data_format)
            if not 'title' in data:
                return send_error(message=constants.msg_must_contain_title)
            if not 'fixed_topic_id' in data:
                return send_error(message=constants.msg_must_contain_fixed_topic_id)
            if not 'topic_ids' in data:
                return send_error(message=constants.msg_must_contain_topics_id)

            current_user = g.current_user
            data['user_id'] = current_user.id
            data['title'] = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", data['title'])
            data['title'] = data['title'].strip()
            is_sensitive = check_sensitive(data['title'])
            if is_sensitive:
                return send_error(message=constants.msg_insensitive_title)

            article = Article.query.filter(Article.title == data['title']).first()
            if article:  # the article does not exist
                return send_error(message=constants.msg_article_already_exists.format(data['title']))

            article, topic_ids = self._parse_article(data=data, article=None)

            # check sensitive words
            is_sensitive = check_sensitive(' '.join(BeautifulSoup(article.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=constants.msg_insensitive_body)

            # only allowed Vietnamese or English article title name
            parent_topic = Topic.query.filter(Topic.id == article.fixed_topic_id).first()
            if parent_topic is not None and parent_topic.name != 'Ngôn ngữ' and parent_topic.name != 'Văn hóa trong và ngoài nước':
                spelling_errors = check_spelling(article.title)
                if len(spelling_errors) > 0:
                    return send_error(message='Article title is spelled wrongly!', data=spelling_errors)


            if article.scheduled_date and article.scheduled_date < datetime.now():
                return send_error(message=messages.ERR_ISSUE.format('Scheduled date is earlier than current time'))

            db.session.add(article)
            db.session.commit()
            # Add topics and get back list of topic for article
            try:
                result = article._asdict()
                result['user'] = article.user
                result['topics'] = article.topics
                
                # upvote/downvote status for current user
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                ArticleFavorite.article_id == article.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                if article.user:
                    followers = UserFollow.query.with_entities(UserFollow.follower_id)\
                        .filter(UserFollow.followed_id == article.user.id).all()
                    follower_ids = [follower[0] for follower in followers]
                    new_article_notify_user_list.send(article.id, follower_ids)
                    g.friend_belong_to_user_id = article.user.id
                    friends = UserFriend.query\
                        .filter(\
                            (UserFriend.friended_id == article.user.id) | \
                            (UserFriend.friend_id == article.user.id))\
                        .all()
                    friend_ids = [friend.adaptive_friend_id for friend in friends]
                    new_article_notify_user_list.send(article.id, friend_ids)
                return send_result(message=constants.msg_create_success,
                                    data=marshal(result, ArticleDto.model_article_response))
            except Exception as e:
                print(e)
                return send_result(data=marshal(article, ArticleDto.model_article_response),
                                    message=constants.msg_create_success_without_topics)
        except Exception as e:
            print(e)
            return send_error(message=constants.msg_create_failed)

    def get_query(self):
        query = Article.query.join(User, isouter=True).filter(db.or_(Article.scheduled_date == None, datetime.utcnow() >= Article.scheduled_date))
        query = query.filter(db.or_(Article.user == None, User.is_deactivated != True))
        return query

    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
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
        if params.get('draft') is not None:
            if params.get('draft'):
                query = query.filter(Article.is_draft == True)
            else:
                query = query.filter(Article.is_draft != True)
        if params.get('is_created_by_friend') and g.current_user:
            query = query\
                .join(UserFollow,(UserFollow.followed_id==Article.user_id), isouter=True)\
                .join(UserFriend,((UserFriend.friended_id==Article.user_id) | (UserFriend.friend_id==Article.user_id)), isouter=True)\
                .filter(
                    (UserFollow.follower_id == g.current_user.id) |
                    ((UserFriend.friended_id == g.current_user.id) | (UserFriend.friend_id == g.current_user.id)) |
                    (Article.article_shares.any(ArticleShare.user_id == g.current_user.id))
                )
        if params.get('hot'):
            if g.current_user:
                query = query.join(TopicBookmark, \
                        ((Article.topics.any(Topic.id == TopicBookmark.topic_id)) &\
                            TopicBookmark.user_id == g.current_user.id), \
                        isouter=True)\
                    .order_by(desc(func.field(TopicBookmark.user_id, g.current_user.id)),\
                        desc(text("upvote_count + downvote_count + share_count + favorite_count")))
            else:
                query = query.\
                    order_by(\
                        desc(text("upvote_count + downvote_count + share_count + favorite_count")))

        return query

    def get(self, args):

        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            # get current user voting status for this article
            current_user = g.current_user
            articles = res.get('data')
            results = []
            for article in articles:
                result = article.__dict__
                # get user info
                user = User.query.filter_by(id=article.user_id).first()
                result['user'] = user
                # get all topics that article belongs to
                result['topics'] = article.topics
                # get fixed topic name
                result['fixed_topic'] = article.fixed_topic
                if current_user:
                    vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                    ArticleFavorite.article_id == article.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            
            res['data'] = marshal(results, ArticleDto.model_article_response)
            return res, code
        except Exception as e:
            return send_error(message=constants.msg_search_failed)
    
    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count}, message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load topics. Contact your administrator for solution.")

    def get_by_id(self, object_id):
        try:
            if object_id is None:
                return send_error(message=constants.msg_lacking_id)
            if object_id.isdigit():
                article = Article.query.filter_by(id=object_id).first()
            else:
                article = Article.query.filter_by(slug=object_id).first()
            if article is None:
                return send_error(message=constants.msg_not_found_with_id.format(object_id))
            
            article.views_count += 1
            db.session.commit()
            result = article._asdict()
            # get user info
            result['user'] = article.user
            # get all topics that article belongs to
            result['fixed_topic'] = article.fixed_topic
            result['topics'] = article.topics
            # upvote/downvote status
            current_user = g.current_user
            if current_user:
                vote = ArticleVote.query.filter(ArticleVote.user_id == current_user.id, ArticleVote.article_id == article.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = ArticleFavorite.query.filter(ArticleFavorite.user_id == current_user.id,
                                                ArticleFavorite.article_id == article.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                update_seen_articles.send(article.id, current_user.id)
            return send_result(data=marshal(result, ArticleDto.model_article_response), message='Success')
        except Exception as e:
            print(e)
            pass
    
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
            current_user, _ = current_app.get_logged_user(request)
            query = Article.query
            if args.get('exclude_article_id'):
                query = query.filter(Article.id != args.get('exclude_article_id'))
            title_similarity = db.func.SIMILARITY_STRING(Article.title, title).label('title_similarity')
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
                result['user'] = article.user
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
        try:
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
            # check sensitive before updating
            is_sensitive = check_sensitive(article.title)
            if is_sensitive:
                return send_error(message=constants.msg_update_failed_insensitive_title)
            is_sensitive = check_sensitive(' '.join(BeautifulSoup(article.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=constants.msg_update_failed_insensitive_body)
            # update topics to article_topic table
            article.updated_date = datetime.utcnow()
            article.last_activity = datetime.utcnow()
            db.session.commit()
            
            result = article._asdict()
            # get user info
            result['user'] = article.user
            # get all topics that article belongs to
            result['topics'] = article.topics
            # upvote/downvote status
            try:
                current_user, _ = current_app.get_logged_user(request)
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
            log(1, e)
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

        if 'scheduled_date' in data:
            try:
                article.scheduled_date = dateutil.parser.isoparse(data.get('scheduled_date'))
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
            topic_ids = data['topic_ids']
            # update proposal topics
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            article.topics = topics

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    article.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    print(e.__str__())
                    pass
        return article, topic_ids
