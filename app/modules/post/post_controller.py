#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from app.dramatiq_consumers import update_seen_posts
import json
from datetime import datetime

# third-party modules
import dateutil.parser
from bs4 import BeautifulSoup
from flask import current_app, g, request
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import and_, desc, func, or_, text

# own modules
from common.db import db
from app.constants import messages
from app.modules.post.post_dto import PostDto
from common.controllers.controller import Controller
from common.enum import VotingStatusEnum
from common.models import UserFollow, UserFriend
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import check_sensitive
from common.utils.wasabi import upload_file
from common.utils.util import encode_file_name
from common.utils.file_handler import get_file_name_extension

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Post = db.get_model('Post')

class PostController(Controller):
    allowed_ordering_fields = ['created_date', 'updated_date', 'comment_count', 'favorite_count']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if not 'html' in data or len(data['html']) == 0:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('post content'))

        current_user, _ = current_app.get_logged_user(request)
        data['user_id'] = current_user.id
        try:

            post = self._parse_post(data=data, post=None)
            if check_sensitive(''.join(BeautifulSoup(post.html, 'html.parser').stripped_strings)):
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

            post.created_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.add(post)
            db.session.commit()
            try:
                result = post.__dict__
                user = User.query.filter_by(id=post.user_id).first()
                result['user'] = user
                return send_result(message=messages.MSG_CREATE_SUCCESS.format('Post'),data=marshal(result, PostDto.model_post_response))
            except Exception as e:
                print(e)
                return send_result(data=marshal(post, PostDto.model_post_response), message=messages.MSG_CREATE_SUCCESS_WITH_ISSUE.format('Post', e))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Post', str(e)))


    def get(self, args):

        try:
            # Get search parameters
            user_id, created_date, updated_date, from_date, to_date, draft, is_deleted = None, None, None, None, None, None, None

            if args.get('user_id'):
                try:
                    user_id = int(args['user_id'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('created_date'):
                try:
                    created_date = dateutil.parser.isoparse(args['created_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('updated_date'):
                try:
                    updated_date = dateutil.parser.isoparse(args['updated_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('from_date'):
                try:
                    from_date = dateutil.parser.isoparse(args['from_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('to_date'):
                try:
                    to_date = dateutil.parser.isoparse(args['to_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('draft'):
                try:
                    draft = bool(args['draft'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('is_deleted'):
                try:
                    is_deleted = bool(args['is_deleted'])
                except Exception as e:
                    print(e.__str__())
                    pass

            query = Post.query.join(User, isouter=True).filter(db.or_(Post.scheduled_date == None, datetime.utcnow() >= Post.scheduled_date))
            query = query.filter(db.or_(Post.user == None, User.is_deactivated != True))
            if is_deleted:
                query = query.with_deleted()

            if user_id:
                query = query.filter(Post.user_id == user_id)
            if created_date:
                query = query.filter(Post.created_date == created_date)
            if updated_date:
                query = query.filter(Post.updated_date == updated_date)
            if from_date:
                query = query.filter(Post.created_date >= from_date)
            if to_date:
                query = query.filter(Post.created_date <= to_date)
            if draft is not None:
                if draft:
                    query = query.filter(Post.is_draft == True)
                else:
                    query = query.filter(Post.is_draft != True)

            ordering_fields_desc = args.get('order_by_desc')
            if ordering_fields_desc:
                for ordering_field in ordering_fields_desc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Post, ordering_field)
                        query = query.order_by(db.desc(column_to_sort))

            ordering_fields_asc = args.get('order_by_asc')
            if ordering_fields_asc:
                for ordering_field in ordering_fields_asc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Post, ordering_field)
                        query = query.order_by(db.asc(column_to_sort))
                        
            res, code = paginated_result(query)
            posts = res.get('data')
            results = []
            for post in posts:
                result = post.__dict__
                user = User.query.filter_by(id=post.user_id).first()
                if g.current_user:
                    update_seen_posts.send(post.id, g.current_user.id)
                result['user'] = user
            res['data'] = marshal(results, PostDto.model_post_response)
            return res, code
        except Exception as e:
            return send_error(message=messages.ERR_GET_FAILED.format('Post', str(e)))


    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Post ID"))
        if 'file' not in request.files:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))

        file_type = request.form.get('file_type', None)
        media_file = request.files.get('file', None)
        post = Post.query.filter_by(id=object_id).first()
        if post is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('post', object_id))

        if not media_file:
            return send_error(message=messages.ERR_NO_FILE)
        if not file_type:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file type'))
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            sub_folder = 'post' + '/' + encode_file_name(str(post.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.ERR_ISSUE.format('Could not save your media file.'))

            post.file_url = url
            post.updated_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.commit()
            result = post._asdict()
            result['user'] = post.user
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Post media'), data=marshal(result, PostDto.model_post_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Post media', str(e)))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_LACKING_QUERY_PARAMS)
        if object_id.isdigit():
            post = Post.query.filter_by(id=object_id).first()
        else:
            post = Post.query.filter_by(slug=object_id).first()
        if post is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Post', object_id))
        else:
            try:
                post.views_count += 1
                db.session.commit()
                result = post.__dict__
                result['user'] = post.user
                return send_result(data=marshal(result, PostDto.model_post_response), message='Success')
            except Exception as e:
                print(e)
                pass

  
    def update(self, object_id, data, is_put=False):
        if object_id is None:
            return send_error(message=messages.ERR_LACKING_QUERY_PARAMS)
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            post = Post.query.filter_by(id=object_id).first()
        else:
            post = Post.query.filter_by(slug=object_id).first()
        if post is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Post', object_id))
        if is_put:
            db.session.delete(post)
            return self.create(data)

        post= self._parse_post(data=data, post=post)

        try:

            is_sensitive = check_sensitive(''.join(BeautifulSoup(post.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=messages.ERR_ISSUE.format('Insensitive body'))

            post.updated_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.commit()            
            result = post.__dict__
            result['user'] = post.user
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Post'), data=marshal(result, PostDto.model_post_response))
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=messages.ERR_UPDATE_FAILED.format('Post', str(e)))


    def delete(self, object_id):
        try:
            if object_id.isdigit():
                post = Post.query.filter_by(id=object_id).first()
            else:
                post = Post.query.filter_by(slug=object_id).first()
            if post is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Post', object_id))
            else:
                db.session.delete(post)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format('Post'))
        
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=messages.ERR_DELETE_FAILED.format('Post', str(e)))


    def get_post_of_friend(self,args):
            page = 1
            page_size = 20

            if args.get('page') and args['page'] > 0:
                try:
                    page = args['page']
                except Exception as e:
                    print(e.__str__())
                    pass

            if args.get('per_page') and args['per_page'] > 0 :
                try:
                    page_size = args['per_page']
                except Exception as e:
                    print(e.__str__())
                    pass

            if page > 0 :
                page = page - 1

            current_user, _ = current_app.get_logged_user(request)

            query = db.session.query(Post)\
            .outerjoin(UserFollow,and_(UserFollow.followed_id==Post.user_id, UserFollow.follower_id==current_user.id))\
            .outerjoin(UserFriend,and_(UserFriend.friended_id==Post.user_id and UserFollow.friend_id==current_user.id))\
            .filter(or_(UserFollow.followed_id > 0,UserFriend.friended_id>0))\
            .group_by(Post)\
            .order_by(desc(Post.share_count + Post.favorite_count),desc(Post.created_date))
            posts = query.offset(page * page_size).limit(page_size).all()

            if posts is not None and len(posts) > 0:
                return send_result(data=marshal(posts, PostDto.model_post_response), message='Success')
            else:
                return send_result(message='Could not find any posts')


    def _parse_post(self, data, post=None):
        if post is None:
            post = Post()

        if 'user_id' in data:
            try:
                post.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass

        if 'html' in data:
            post.html = data['html']
            
        if 'is_draft' in data:
            try:
                post.is_draft = bool(data['is_draft'])
            except Exception as e:
                print(e.__str__())
                pass
            
        if 'is_deleted' in data:
            try:
                post.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'allow_favorite' in data:
                try:
                    post.allow_favorite = bool(data['allow_favorite'])
                except Exception as e:
                    print(e.__str__())
                    pass

        return post

