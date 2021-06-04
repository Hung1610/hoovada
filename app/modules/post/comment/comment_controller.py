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
from app.modules.post.comment.comment_dto import CommentDto
from common.controllers.comment_controller import BaseCommentController
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Post = db.get_model('Post')
PostComment = db.get_model('PostComment')

class CommentController(BaseCommentController):

    query_classname = 'PostComment'
    related_field_name = 'post_id'

    def get(self, post_id, args):

        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        try:
            query = PostComment.query
            query = query.join(User, isouter=True).filter(User.is_deactivated == False)
            if post_id is not None:
                query = query.filter(PostComment.post_id == post_id)
            if user_id is not None:
                query = query.filter(PostComment.user_id == user_id)
                
            comments = query.all()
            if comments is not None and len(comments) > 0:
                results = list()
                for comment in comments:
                    result = comment._asdict()
                    user = User.query.filter_by(id=comment.user_id).first()
                    result['user'] = user
                    results.append(result)
                return send_result(marshal(results, CommentDto.model_response), message=messages.MSG_GET_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))



    def create(self, post_id, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'comment' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('comment'))

        current_user = g.current_user
        data['user_id'] = current_user.id
        data['post_id'] = post_id

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

            result = comment._asdict()
            user = User.query.filter_by(id=comment.user_id).first()
            result['user'] = user
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, CommentDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        comment = PostComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        try:
            result = comment._asdict()
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
        
        comment = PostComment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user 
        if current_user and current_user.id != comment.user_id:
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        comment = self._parse_comment(data=data, comment=comment)   
        try:
            comment.updated_date = datetime.utcnow()
            db.session.commit()
            result = comment._asdict()
            user = User.query.filter_by(id=comment.user_id).first()
            result['user'] = user
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, CommentDto.model_response))

        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        try:
            comment = PostComment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            db.session.delete(comment)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))
