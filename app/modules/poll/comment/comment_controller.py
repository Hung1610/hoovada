#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from re import sub

# third-party modules
from flask import current_app, request
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.poll.comment.comment_dto import CommentDto
from common.controllers.comment_controller import BaseCommentController
from common.utils.response import send_error, send_result
from common.utils.sensitive_words import check_sensitive

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Post = db.get_model('Post')
PollComment = db.get_model('PollComment')


class CommentController(BaseCommentController):

    query_classname = 'PollComment'
    related_field_name = 'poll_id'

    def get(self, poll_id, args):

        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = PollComment.query
        if poll_id is not None:
            query = query.filter(PollComment.poll_id == poll_id)
        if user_id is not None:
            query = query.filter(PollComment.user_id == user_id)
            
        comments = query.all()
        if comments is not None and len(comments) > 0:
            results = list()
            for comment in comments:
                result = comment.__dict__
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                results.append(result)
            return send_result(marshal(results, CommentDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any comments.')

    def create(self, poll_id, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'comment' in data:
            return send_error(message="The comment body must be included")

        current_user, _ = current_app.get_logged_user(request)
        if current_user is None:
            return send_error(message=messages.ERR_NOT_LOGIN)

        data['user_id'] = current_user.id
        data['poll_id'] = poll_id

        try:
            comment = self._parse_comment(data=data, comment=None)
            is_sensitive = check_sensitive(sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "",comment.comment))
            if is_sensitive:
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)


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
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(message='PollComment was created successfully', data=marshal(result, CommentDto.model_response))
            except Exception as e:
                print(e.__str__())
                return send_result(data=marshal(comment, CommentDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create comment')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error('PollComment ID is null')
        comment = PollComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message='Could not find comment with the ID {}'.format(object_id))
        else:
            try:
                result = comment.__dict__
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(data=marshal(result, CommentDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not get comment with the ID {}'.format(object_id))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='PollComment ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        current_user, _ = current_app.get_logged_user(request)
        if not current_user:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
        try:
            comment = PollComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='PollComment with the ID {} not found.'.format(object_id))
            if current_user and current_user.id != comment.user_id:
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)
            else:
                comment = self._parse_comment(data=data, comment=comment)

                is_sensitive = check_sensitive(sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", comment.comment))
                if is_sensitive:
                    return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

                comment.updated_date = datetime.utcnow()
                db.session.commit()
                result = comment.__dict__
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(message='Update successfully', data=marshal(result, CommentDto.model_response))
        
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(code=500, message='Could not update comment.')

    def delete(self, object_id):
        try:
            comment = PollComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='PollComment with the ID {} not found.'.format(object_id))
            else:
                # ---------Delete from other tables----------#
                # delete from share
                # delete favorite

                db.session.delete(comment)
                db.session.commit()
                return send_result(message='PollComment with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete comment with the ID {}.'.format(object_id))
