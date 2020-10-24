#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from slugify import slugify
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal
from sqlalchemy import desc, text, func, and_, or_
from bs4 import BeautifulSoup

# own modules
from app import db
from app.constants import messages
from app.modules.post.post import Post
from app.modules.post.post_dto import PostDto
from app.modules.post.voting.vote import PostVote, VotingStatusEnum
from app.modules.auth.auth_controller import AuthController
from app.common.controller import Controller
from app.modules.topic.topic import Topic
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive
from app.modules.topic.bookmark.bookmark import TopicBookmark
from app.modules.user.friend.friend import UserFriend
from app.modules.user.follow.follow import UserFollow


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class PostController(Controller):
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
        if not 'title' in data:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('title'))

        current_user, _ = AuthController.get_logged_user(request)
        data['user_id'] = current_user.id
        try:
            is_sensitive = check_sensitive(data['title'])
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Title is too sensitive'))

            post = Post.query.filter(Post.title == data['title']).filter(Post.user_id == data['user_id']).first()
            if post:
                return send_error(message=messages.MSG_ALREADY_EXISTS.format('Post'))
            post, topic_ids = self._parse_post(data=data, post=None)
            is_sensitive = check_sensitive(''.join(BeautifulSoup(post.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Post body is too sensitive'))
            post.created_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.add(post)
            db.session.commit()
            # Add topics and get back list of topic for post
            try:
                result = post.__dict__
                # get user info
                user = User.query.filter_by(id=post.user_id).first()
                result['user'] = user
                # add post_topics
                topics = []
                for topic_id in topic_ids:
                    try:
                        topic = Topic.query.filter_by(id=topic_id).first()
                        post.topics.append(topic)
                        db.session.commit()
                        topics.append(topic)
                    except Exception as e:
                        print(e)
                        pass
                result['topics'] = topics
                
                # upvote/downvote status for current user
                vote = PostVote.query.filter(PostVote.user_id == current_user.id, PostVote.post_id == post.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                return send_result(message=messages.MSG_CREATE_SUCCESS.format('Post'),
                                    data=marshal(result, PostDto.model_post_response))
            except Exception as e:
                print(e)
                return send_result(data=marshal(post, PostDto.model_post_response),
                                    message=messages.MSG_CREATE_SUCCESS_WITH_ISSUE.format('Post', e))
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=messages.MSG_CREATE_FAILED.format('Post', e))

    def get(self, args):
        """
        Search posts.
        :param args:
        :return:
        """
        try:
            # Get search parameters
            title, user_id, fixed_topic_id, created_date, updated_date, from_date, to_date, topic_ids, draft, is_deleted = None, None, None, None, None, None, None, None, None, None
            if args.get('title'):
                title = args['title']
            if args.get('user_id'):
                try:
                    user_id = int(args['user_id'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('fixed_topic_id'):
                try:
                    fixed_topic_id = int(args['fixed_topic_id'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('created_date'):
                try:
                    created_date = dateutil.parser.isoparse(args['created_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('updated_date'):
                try:
                    updated_date = dateutil.parser.isoparse(args['updated_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('from_date'):
                try:
                    from_date = dateutil.parser.isoparse(args['from_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('to_date'):
                try:
                    to_date = dateutil.parser.isoparse(args['to_date'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('topic_id'):
                try:
                    topic_ids = args['topic_id']
                except Exception as e:
                    print(e)
                    pass
            if args.get('draft'):
                try:
                    draft = bool(args['draft'])
                except Exception as e:
                    print(e)
                    pass
            if args.get('is_deleted'):
                try:
                    is_deleted = bool(args['is_deleted'])
                except Exception as e:
                    print(e)
                    pass

            query = Post.query.join(User, isouter=True).filter(db.or_(Post.scheduled_date == None, datetime.utcnow() >= Post.scheduled_date))
            query = query.filter(db.or_(Post.user == None, User.is_deactivated != True))
            if not is_deleted:
                query = query.filter(Post.is_deleted != True)
            else:
                query = query.filter(Post.is_deleted == True)
            if title and not str(title).strip().__eq__(''):
                title = '%' + title.strip() + '%'
                query = query.filter(Post.title.like(title))
            if user_id:
                query = query.filter(Post.user_id == user_id)
            if fixed_topic_id:
                query = query.filter(Post.fixed_topic_id == fixed_topic_id)
            if created_date:
                query = query.filter(Post.created_date == created_date)
            if updated_date:
                query = query.filter(Post.updated_date == updated_date)
            if from_date:
                query = query.filter(Post.created_date >= from_date)
            if to_date:
                query = query.filter(Post.created_date <= to_date)
            if topic_ids:
                query = query.filter(Post.topics.any(Topic.id.in_(topic_ids)))
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
                        
            posts = query.all()
            results = []
            for post in posts:
                result = post.__dict__
                # get user info
                user = User.query.filter_by(id=post.user_id).first()
                result['user'] = user
                # get all topics that post belongs to
                result['topics'] = post.topics
                # get fixed topic name
                result['fixed_topic_name'] = post.fixed_topic.name
                # get current user voting status for this post
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = PostVote.query.filter(PostVote.user_id == current_user.id, PostVote.post_id == post.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                results.append(result)
            return send_result(marshal(results, PostDto.model_post_response), message='Success')
        except Exception as e:
            return send_error(message=messages.MSG_CREATE_SUCCESS.format('Post'))

    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.MSG_PLEASE_PROVIDE.format("Post ID"))
        if 'file' not in request.files:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('file'))

        file_type = request.form.get('file_type', None)
        media_file = request.files.get('file', None)
        post = Post.query.filter_by(id=object_id).first()
        if post is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('post', object_id))

        if not media_file:
            return send_error(message=messages.MSG_NO_FILE)
        if not file_type:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('file type'))
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            bucket = 'hoovada'
            sub_folder = 'post' + '/' + encode_file_name(str(post.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.MSG_ISSUE.format('Could not save your media file.'))

            post.file_url = url
            post.updated_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.commit()
            result = post._asdict()
            # update user information for post
            result['user'] = post.user
            # khi moi tao thi gia tri up_vote va down_vote cua nguoi dung hien gio la False
            result['up_vote'] = False
            result['down_vote'] = False
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Post media'), data=marshal(result, PostDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Post media', e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.MSG_LACKING_QUERY_PARAMS)
        if object_id.isdigit():
            post = Post.query.filter_by(id=object_id).first()
        else:
            post = Post.query.filter_by(slug=object_id).first()
        if post is None:
            return send_error(message=messages.msg_not_found_with_id.format(object_id))
        else:
            post.views_count += 1
            db.session.commit()
            result = post.__dict__
            # get user info
            result['user'] = post.user
            # get all topics that post belongs to
            result['topics'] = post.topics
            # upvote/downvote status
            try:
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = PostVote.query.filter(PostVote.user_id == current_user.id, PostVote.post_id == post.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            except Exception as e:
                print(e)
                pass
            return send_result(data=marshal(result, PostDto.model_post_response), message='Success')
    
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
            current_user, _ = AuthController.get_logged_user(request)
            query = Post.query
            title_similarity = db.func.SIMILARITY_STRING(title, Post.title).label('title_similarity')
            query = query.with_entities(Post, title_similarity)\
                .filter(title_similarity > 50)
            if fixed_topic_id:
                query = query.filter(Post.fixed_topic_id == fixed_topic_id)
            if topic_ids:
                query = query.filter(Post.topics.any(Topic.id.in_(topic_ids)))
            posts = query\
                .order_by(desc(title_similarity))\
                .limit(limit)\
                .all()
            results = list()
            for post in posts:
                post = post[0]
                result = post._asdict()
                # get user info
                result['user'] = post.user
                result['topics'] = post.topics
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    vote = PostVote.query.filter(PostVote.user_id == current_user.id, PostVote.post_id == post.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                results.append(result)
            return send_result(data=marshal(results, PostDto.model_post_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get similar posts failed. Error: "+ e.__str__())

    def update(self, object_id, data, is_put=False):
        if object_id is None:
            return send_error(message=messages.MSG_LACKING_QUERY_PARAMS)
        if not isinstance(data, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            post = Post.query.filter_by(id=object_id).first()
        else:
            post = Post.query.filter_by(slug=object_id).first()
        if post is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Post', object_id))
        if is_put:
            db.session.delete(post)
            return self.create(data)
        post, _ = self._parse_post(data=data, post=post)

        if 'topic_ids' in data:
            topic_ids = data['topic_ids']
            # update post topics
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            post.topics = topics
        try:
            # check sensitive before updating
            is_sensitive = check_sensitive(post.title)
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Insensitive title'))
            is_sensitive = check_sensitive(''.join(BeautifulSoup(post.html, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Insensitive body'))
            # update topics to post_topic table
            post.updated_date = datetime.utcnow()
            post.last_activity = datetime.utcnow()
            db.session.commit()
            
            result = post.__dict__
            # get user info
            result['user'] = post.user
            # get all topics that post belongs to
            result['topics'] = post.topics
            # upvote/downvote status
            try:
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = PostVote.query.filter(PostVote.user_id == current_user.id, PostVote.post_id == post.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            except Exception as e:
                print(e)
                pass
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Post'),
                                data=marshal(result, PostDto.model_post_response))
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_UPDATE_FAILED.format('Post', e))

    def delete(self, object_id):
        try:
            if object_id.isdigit():
                post = Post.query.filter_by(id=object_id).first()
            else:
                post = Post.query.filter_by(slug=object_id).first()
            if post is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Post', object_id))
            else:
                db.session.delete(post)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS.format('Post'))
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_DELETE_FAILED.format('Post', e))

    def update_slug(self):
        posts = Post.query.all()
        try:
            for post in posts:
                post.slug = slugify(post.title)
                db.session.commit()
            return send_result(marshal(posts, PostDto.model_post_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

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

            current_user, _ = AuthController.get_logged_user(request)

            query = db.session.query(Post)\
            .outerjoin(UserFollow,and_(UserFollow.followed_id==Post.user_id, UserFollow.follower_id==current_user.id))\
            .outerjoin(UserFriend,and_(UserFriend.friended_id==Post.user_id and UserFollow.friend_id==current_user.id))\
            .filter(or_(UserFollow.followed_id > 0,UserFriend.friended_id>0))\
            .group_by(Post)\
            .order_by(desc(Post.upvote_count + Post.downvote_count + Post.share_count + Post.favorite_count),desc(Post.created_date))
            posts = query.offset(page * page_size).limit(page_size).all()

            if posts is not None and len(posts) > 0:
                return send_result(data=marshal(posts, PostDto.model_post_response), message='Success')
            else:
                return send_result(message='Could not find any posts')

    def _parse_post(self, data, post=None):
        if post is None:
            post = Post()
        if 'title' in data:
            try:
                post.title = data['title']
            except Exception as e:
                print(e)
                pass
        if 'user_id' in data:
            try:
                post.user_id = data['user_id']
            except Exception as e:
                print(e)
                pass
        if 'fixed_topic_id' in data:
            try:
                post.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e)
                pass
        if 'html' in data:
            post.html = data['html']

        if 'scheduled_date' in data:
            try:
                post.scheduled_date = data['scheduled_date']
            except Exception as e:
                print(e)
                pass
            
        if 'is_draft' in data:
            try:
                post.is_draft = bool(data['is_draft'])
            except Exception as e:
                print(e)
                pass
            
        if 'is_deleted' in data:
            try:
                post.is_deleted = bool(data['is_deleted'])
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
        return post, topic_ids

