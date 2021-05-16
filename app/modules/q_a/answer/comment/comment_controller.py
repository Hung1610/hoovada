#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from flask_restx import marshal

# own modules
from common.utils.onesignal_notif import push_notif_to_specific_users
from app.constants import messages
from common.db import db
from app.constants import messages
from app.modules.q_a.answer.comment.comment_dto import CommentDto
from common.controllers.comment_controller import BaseCommentController
from common.utils.response import send_error, send_result
from common.utils.sensitive_words import is_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


AnswerCommentFavorite = db.get_model('AnswerCommentFavorite')
Answer = db.get_model('Answer')
AnswerComment = db.get_model('AnswerComment')
User = db.get_model('User')


class CommentController(BaseCommentController):
    '''Controller for answer comments'''

    query_classname = 'AnswerComment'
    related_field_name = 'answer_id'

    def get(self, answer_id, args):

        current_user = g.current_user
        user_id = None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = AnswerComment.query
        query = query.join(User, isouter=True).filter(User.is_deactivated == False)
        if answer_id is not None:
            query = query.filter(AnswerComment.answer_id == answer_id)
        if user_id is not None:
            query = query.filter(AnswerComment.user_id == user_id)
            
        comments = query.all()
        if comments is not None and len(comments) > 0:
            results = list()
            for comment in comments:
                result = comment.__dict__
                result['user'] = comment.user
                if current_user:
                    favorite = AnswerCommentFavorite.query.filter(AnswerCommentFavorite.user_id == current_user.id,
                                                    AnswerCommentFavorite.answer_comment_id == comment.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            return send_result(marshal(results, CommentDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any comments.')

    def create(self, answer_id, data):
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'comment' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('comment'))

        if is_sensitive(data['comment']):
            return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        current_user = g.current_user
        data['user_id'] = current_user.id
        
        answer = Answer.query.filter(Answer.id == answer_id).first()
        if not answer:
            return send_error(message='The answer does not exist.')
        
        if (not answer.allow_comments):
            return send_error(message='This answer does not allow commenting.')
        data['answer_id'] = answer_id

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

            try:
                result = comment.__dict__
                result['user'] = comment.user
                if comment.answer.user:                    
                    if comment.answer.user.is_online and comment.answer.user.new_answer_comment_notify_settings:
                        display_name =  comment.user.display_name if comment.user else 'Khách'
                        message = display_name + ' đã bình luận câu trả lời!'
                        push_notif_to_specific_users(message, [comment.answer.user_id])
                return send_result(message='AnswerComment was created successfully', data=marshal(result, CommentDto.model_response))
            except Exception as e:
                print(e.__str__())
                return send_result(data=marshal(comment, CommentDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create comment')


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error('AnswerComment ID is null')
        comment = AnswerComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message='Could not find comment with the ID {}'.format(object_id))

        current_user = g.current_user 
        try:
            result = comment.__dict__
            result['user'] = comment.user
            if current_user:
                favorite = AnswerCommentFavorite.query.filter(AnswerCommentFavorite.user_id == current_user.id,
                                                AnswerCommentFavorite.answer_comment_id == comment.id).first()
                result['is_favorited_by_me'] = True if favorite else False
            return send_result(data=marshal(result, CommentDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get comment with the ID {}'.format(object_id))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('object_id'))
        
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        comment = AnswerComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message='AnswerComment with the ID {} not found.'.format(object_id))
        
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
            result['user'] = comment.user
            if current_user:
                favorite = AnswerCommentFavorite.query.filter(AnswerCommentFavorite.user_id == current_user.id,
                                                AnswerCommentFavorite.answer_comment_id == comment.id).first()
                result['is_favorited_by_me'] = True if favorite else False
            return send_result(message='Update successfully', data=marshal(result, CommentDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update comment.')


    def delete(self, object_id):
        try:
            comment = AnswerComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='AnswerComment with the ID {} not found.'.format(object_id))
            else:
                # ---------Delete from other tables----------#
                # delete from vote

                # delete from share

                # delete favorite

                db.session.delete(comment)
                db.session.commit()
                return send_result(message='AnswerComment with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete comment with the ID {}.'.format(object_id))
