#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from app.constants import messages
from common.db import db
from app.modules.article.comment.comment_dto import CommentDto
from common.utils.onesignal_notif import push_notif_to_specific_users
from common.controllers.comment_controller import BaseCommentController
from common.models import Article, ArticleComment, User
from common.utils.response import send_error, send_result
from common.utils.sensitive_words import is_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CommentController(BaseCommentController):
    '''Controller for article comments'''
    query_classname = 'ArticleComment'
    related_field_name = 'article_id'
    
    def get(self, article_id, args):
        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        try:
            query = ArticleComment.query
            query = query.join(User, isouter=True).filter(User.is_deactivated == False)
            if article_id is not None:
                query = query.filter(ArticleComment.article_id == article_id)
            if user_id is not None:
                query = query.filter(ArticleComment.user_id == user_id)
                
            comments = query.all()
            if comments is not None and len(comments) > 0:
                results = list()
                for comment in comments:
                    result = comment.__dict__
                    user = User.query.filter_by(id=comment.user_id).first()
                    result['user'] = user
                    results.append(result)
                return send_result(marshal(results, CommentDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, article_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'comment' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('comment'))

        if is_sensitive(data['comment']):
            return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        current_user = g.current_user
        data['user_id'] = current_user.id

        article = Article.query.filter(Article.id == article_id).first()
        if not article:
            return send_error(message=messages.ERR_NOT_FOUND)
        
        if article.allow_comments is not None and article.allow_comments is False:
            return send_error(message=messages.ERR_COMMENT_NOT_ALLOWED)

        data['article_id'] = article_id

        try:
            comment = self._parse_comment(data=data, comment=None)
            comment.created_date = datetime.utcnow()
            comment.updated_date = datetime.utcnow()
            db.session.add(comment)
            
            try:
                user = User.query.filter_by(id=comment.user_id).first()
                user.comment_count += 1
            except Exception as e:
                print(e.__str__())
                pass

            db.session.commit()

            result = comment.__dict__
            result['user'] = comment.user
            if comment.article.user:
                if comment.article.user.is_online and comment.article.user.new_article_comment_notify_settings:
                    display_name =  comment.user.display_name if comment.user else 'Khách'
                    message = display_name + ' có bình luận bài viết!'
                    push_notif_to_specific_users(message, [comment.article.user_id])

            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, CommentDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        comment = ArticleComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        try:
            result = comment.__dict__
            user = User.query.filter_by(id=comment.user_id).first()
            result['user'] = user
            return send_result(data=marshal(result, CommentDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
        
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        comment = ArticleComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user 
        if current_user and current_user.id != comment.user_id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        
        if 'comment' in data:
            if is_sensitive(data['comment']):
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        comment = self._parse_comment(data=data, comment=comment)
        try:
            comment.updated_date = datetime.utcnow()
            db.session.commit()
            result = comment.__dict__
            user = User.query.filter_by(id=comment.user_id).first()
            result['user'] = user
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CommentDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        try:
            comment = ArticleComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(comment)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
