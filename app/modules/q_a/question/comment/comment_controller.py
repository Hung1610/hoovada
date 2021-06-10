#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from common.db import db
from common.cache import cache
from app.constants import messages
from app.modules.q_a.question.comment.comment_dto import CommentDto
from common.dramatiq_producers import push_notif_to_specific_users_produce
from common.controllers.comment_controller import BaseCommentController
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Question = db.get_model('Question')
QuestionComment = db.get_model('QuestionComment')
User = db.get_model('User')


class CommentController(BaseCommentController):

    query_classname = 'QuestionComment'
    related_field_name = 'question_id'

    def get(self, question_id, args):

        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        try:
            current_user = g.current_user 
            query = QuestionComment.query
            query = query.join(User, isouter=True).filter(User.is_deactivated == False)
            if question_id is not None:
                query = query.filter(QuestionComment.question_id == question_id)
                
            if user_id is not None:
                query = query.filter(QuestionComment.user_id == user_id)
                
            comments = query.all()
            if comments is not None and len(comments) > 0:
                results = list()
                for comment in comments:
                    result = comment._asdict()
                    result['user'] = comment.user
                        
                    results.append(result)
                return send_result(marshal(results, CommentDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create(self, question_id, data):
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'comment' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('comment'))


        question = Question.query.filter(Question.id == question_id).first()
        if question is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        
        if question.allow_comments is False:
            return send_error(message=messages.ERR_COMMENT_NOT_ALLOWED)
        
        current_user = g.current_user
        data['user_id'] = current_user.id
        data['question_id'] = question_id

        try:
            comment = self._parse_comment(data=data, comment=None)
            comment.created_date = datetime.utcnow()
            comment.updated_date = datetime.utcnow()
            db.session.add(comment)
            user = User.query.filter_by(id=comment.user_id).first()
            user.comment_count += 1
            
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)

            # notification
            try:
                if comment.question.user and comment.question.user.is_online and comment.question.user.new_question_comment_notify_settings:
                    display_name =  comment.user.display_name if comment.user else 'Khách'
                    message = display_name + ' đã bình luận câu hỏi!'
                    push_notif_to_specific_users_produce(message, [comment.question.user_id])
            except Exception as e:
                print(e.__str__())
                pass

            result = comment._asdict()
            result['user'] = comment.user
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        current_user = g.current_user 
        comment = QuestionComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        try:
            result = comment._asdict()
            result['user'] = comment.user
            return send_result(data=marshal(result, CommentDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=ERR_GET_FAILED.format(object_id, str(e)))


    def update(self, object_id, data):

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))


        comment = QuestionComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        

        current_user = g.current_user 
        if current_user and current_user.id != comment.user_id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        
        try:
            comment = self._parse_comment(data=data, comment=comment)
            comment.updated_date = datetime.utcnow()
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)
            result = comment._asdict()
            result['user'] = comment.user
            
            return send_result()
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        try:
            comment = QuestionComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message=messages.ERR_NOT_FOUND)
        
            db.session.delete(comment)
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)
            return send_result()

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
