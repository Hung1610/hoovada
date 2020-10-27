#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal
from flask import request, current_app

# own modules
from app import db
from common.controllers.comment_controller import BaseCommentController
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.answer.comment.favorite.favorite import AnswerCommentFavorite
from common.models import AnswerComment
from app.modules.q_a.answer.comment.comment_dto import CommentDto
from common.models import User
from common.utils.response import send_error, send_result
from common.utils.sensitive_words import check_sensitive
from common.utils.types import UserRole, PermissionType
from common.utils.permission import has_permission
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CommentController(BaseCommentController):
    '''
    Controller for answer comments
    '''
    query_classname = 'AnswerComment'
    related_field_name = 'answer_id'

    def get(self, answer_id, args):
        """
        Search comments by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        # user_id, question_id, answer_id = None, None, None

        current_user, _ = current_app.get_logged_user(request)
        user_id = None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = AnswerComment.query
        query = query.join(User, isouter=True).filter(db.or_(AnswerComment.user == None, User.is_deactivated != True))
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
        current_user, _ = current_app.get_logged_user(request)
        # Check is admin or has permission
        if not (UserRole.is_admin(current_user.admin)
                or has_permission(current_user.id, PermissionType.ANSWER_COMMENT)):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'comment' in data:
            return send_error(message="The comment body must be included")

        current_user, _ = current_app.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id
        answer = Answer.query.filter(Answer.id == answer_id).first()
        if not answer:
            return send_error(message='The answer does not exist.')
        if not answer.question.allow_comments:
            return send_error(message='This question does not allow commenting.')
        if not answer.allow_comments:
            return send_error(message='This answer does not allow commenting.')
        data['answer_id'] = answer_id

        try:
            comment = self._parse_comment(data=data, comment=None)
            is_sensitive = check_sensitive(comment.comment)
            if is_sensitive:
                return send_error(message='Insensitive contents not allowed.')
            comment.created_date = datetime.utcnow()
            comment.updated_date = datetime.utcnow()
            db.session.add(comment)
            db.session.commit()
            # update comment count for user
            try:
                user = User.query.filter_by(id=comment.user_id).first()
                user.comment_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                pass

            try:
                result = comment.__dict__
                # get thong tin user
                result['user'] = comment.user
                return send_result(message='AnswerComment was created successfully',
                                   data=marshal(result, CommentDto.model_response))
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

        current_user, _ = current_app.get_logged_user(request)
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
            return send_error(message='AnswerComment ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        current_user, _ = current_app.get_logged_user(request)
        try:
            comment = AnswerComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='AnswerComment with the ID {} not found.'.format(object_id))
            else:
                comment = self._parse_comment(data=data, comment=comment)
                is_sensitive = check_sensitive(comment.comment)
                if is_sensitive:
                    return send_error(message='Insensitive contents not allowed.')
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
