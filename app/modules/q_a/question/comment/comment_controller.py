#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal
from flask import request

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.question.question import Question
from app.modules.q_a.question.comment.favorite.favorite import QuestionCommentFavorite
from app.modules.q_a.question.comment.comment import QuestionComment
from app.modules.q_a.question.comment.comment_dto import CommentDto
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CommentController(Controller):
    def get(self, question_id, args):
        """
        Search comments by params.

        :param args: Arguments in dictionary form.

        :return:
        """
        # user_id, question_id, question_id = None, None, None
        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        current_user, _ = AuthController.get_logged_user(request)

        query = QuestionComment.query
        query = query.join(User).filter(db.or_(QuestionComment.user == None, User.is_deactivated != True))
        if question_id is not None:
            query = query.filter(QuestionComment.question_id == question_id)
        if user_id is not None:
            query = query.filter(QuestionComment.user_id == user_id)
            
        comments = query.all()
        if comments is not None and len(comments) > 0:
            results = list()
            for comment in comments:
                result = comment.__dict__
                result['user'] = comment.user
                if current_user:
                    favorite = QuestionCommentFavorite.query.filter(QuestionCommentFavorite.user_id == current_user.id,
                                                    QuestionCommentFavorite.question_comment_id == comment.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            return send_result(marshal(results, CommentDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any comments.')

    def create(self, question_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'comment' in data:
            return send_error(message="The comment body must be included")

        current_user, _ = AuthController.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id
        question = Question.query.filter(Question.id == question_id).first()
        if not question:
            return send_error(message='The question does not exist.')
        if not question.allow_comments: 
            return send_error(message='This question does not allow commenting.')
        data['question_id'] = question_id

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
                result['user'] = comment.user
                return send_result(message='QuestionComment was created successfully',
                                   data=marshal(result, CommentDto.model_response))
            except Exception as e:
                print(e.__str__())
                return send_result(data=marshal(comment, CommentDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create comment')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error('QuestionComment ID is null')

        current_user, _ = AuthController.get_logged_user(request)

        comment = QuestionComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message='Could not find comment with the ID {}'.format(object_id))
        else:
            try:
                result = comment.__dict__
                result['user'] = comment.user
                if current_user:
                    favorite = QuestionCommentFavorite.query.filter(QuestionCommentFavorite.user_id == current_user.id,
                                                    QuestionCommentFavorite.question_comment_id == comment.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                return send_result(data=marshal(result, CommentDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not get comment with the ID {}'.format(object_id))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='QuestionComment ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')

        current_user, _ = AuthController.get_logged_user(request)

        try:
            comment = QuestionComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='QuestionComment with the ID {} not found.'.format(object_id))
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
                    favorite = QuestionCommentFavorite.query.filter(QuestionCommentFavorite.user_id == current_user.id,
                                                    QuestionCommentFavorite.question_comment_id == comment.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                return send_result(message='Update successfully', data=marshal(result, CommentDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update comment.')

    def delete(self, object_id):
        try:
            comment = QuestionComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='QuestionComment with the ID {} not found.'.format(object_id))
            else:
                # ---------Delete from other tables----------#
                # delete from vote

                # delete from share

                # delete favorite

                db.session.delete(comment)
                db.session.commit()
                return send_result(message='QuestionComment with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete comment with the ID {}.'.format(object_id))

    def _parse_comment(self, data, comment=None):
        if comment is None:
            comment = QuestionComment()
        if 'comment' in data:
            comment.comment = data['comment']
        if 'question_id' in data:
            try:
                comment.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            try:
                comment.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return comment
