#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import ast
from slugify import slugify
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import marshal
import dateutil.parser
from sqlalchemy import or_, and_, func, desc, text

# own modules
from app.common.controller import Controller
from app.modules.auth.auth_controller import AuthController
from app.modules.topic.topic import Topic, TopicUserEndorse
from app.modules.topic.topic_dto import TopicDto
from app import db
from app.utils.response import send_error, send_result, send_paginated_result, paginated_result
from app.modules.user.user import User
from app.modules.user.follow.follow import UserFollow
from app.utils.sensitive_words import check_sensitive
from app.utils.file_handler import append_id, get_file_name_extension
from app.utils.util import encode_file_name
from app.utils.wasabi import upload_file
from app.constants import messages
from app.modules.topic.question_topic.question_topic import QuestionTopic
from app.modules.topic.article_topic.article_topic import ArticleTopic
from app.modules.topic.bookmark.bookmark import TopicBookmark

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class TopicController(Controller):

    def create_topics(self):
        fixed_topics = ["Những lĩnh vực khác",
                        "hoovada.com", 
                        "Du lịch", 
                        "Gia đình & Quan hệ xã hội", 
                        "Giáo dục & Tham khảo",
                        "Giải trí & Âm nhạc",
                        "Khoa học Tự nhiên", 
                        "Khoa học Xã hội", 
                        "Kinh doanh & Tài chính", 
                        "Máy tính & Internet",
                        "Môi trường", 
                        "Nhà & Vườn", 
                        "Nơi ăn uống", 
                        "Sức khỏe",
                        "Thai nghén & Nuôi dạy con", 
                        "Thể thao", 
                        "Thủ tục hành chính", 
                        "Tin tức & Sự kiện",
                        "Trò chơi & Giải trí", 
                        "Văn hóa & Xã hội", 
                        "Văn học & Nhân văn", 
                        "Vật nuôi",
                        "Vẻ đẹp & Phong cách", 
                        "Ô-tô & Vận tải", 
                        "Điện tử tiêu dùng", 
                        "Ẩm thực", 
                        "Doanh nghiệp địa phương",  
                        "Chính trị",
                        "Tôn giáo",
                        "Đời tư",
                        "Lĩnh vực người lớn"]

        try:
            for topic_name in fixed_topics:
                topic = Topic.query.filter(Topic.name == topic_name, Topic.is_fixed == True).first()
                if not topic:  # the topic does not exist
                    topic = Topic(name=topic_name, is_fixed=True, user_id=3)
                    db.session.add(topic)
                    db.session.commit()
        except Exception as e:
            print(e.__str__())
            pass

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Could not parse the params')
        name, user_id, parent_id, is_fixed = None, None, None, None
        current_user, _ = AuthController.get_logged_user(request)
        if 'name' in args:
            name = args['name']
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
        if 'parent_id' in args:
            try:
                parent_id = int(args['parent_id'])
            except Exception as e:
                print(e.__str__())
        if 'is_fixed' in args:
            try:
                is_fixed = int(args['is_fixed'])
            except Exception as e:
                print(e.__str__())
        if name is None and user_id is None and parent_id is None and is_fixed is None:
            return send_error(message='Please provide params to search.')
        query = db.session.query(Topic)
        is_filter = False
        if name is not None and not str(name).strip().__eq__(''):
            name = '%' + name.strip() + '%'
            query = query.filter(Topic.name.like(name))
            is_filter = True
        if user_id is not None:
            query = query.filter(Topic.user_id == user_id)
            is_filter = True
        if parent_id is not None:
            query = query.filter(Topic.parent_id == parent_id)
            is_filter = True
        if is_fixed is not None:
            query = query.filter(Topic.is_fixed == is_fixed)
            is_filter = True

        # default: "Những lĩnh vực khác" trên frontend
        if is_filter:
            topics = query.order_by(desc(func.field(Topic.name, "Những lĩnh vực khác"))).all()
            if topics is not None and len(topics) > 0:
                return send_result(marshal(topics, TopicDto.model_topic_response), message='Success')
            else:
                return send_error(message='Could not find any topics.')

        else:
            return send_error(message='Could not find topics with these parameters.')


    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        
        if not 'name' in data:
            return send_error(message='Topic name must be filled')
        else:
            topic_name = data['name']
            is_sensitive = check_sensitive(topic_name)
            if is_sensitive:
                return send_error(message='Nội dung chủ đề mới tạo không hợp lệ.')

        if not 'parent_id' in data:
            return send_error(message='Topic must have a parent topic.')
        try:
            # check topuc already exists
            topic = Topic.query.filter(or_(
                and_(Topic.name == data['name'], Topic.parent_id == data['parent_id']),
                and_(Topic.name == data['name'], Topic.parent_id == None,data['parent_id']==0),
                and_(Topic.name == data['name'], Topic.name == data['name'], int(data['parent_id'])>0))
                ).first()

            if not topic:  # the topic does not exist
                topic = self._parse_topic(data=data, topic=None)
                topic.created_date = datetime.today()

                # capitalize first letter
                topic.name = topic.name.capitalize()
                db.session.add(topic)
                db.session.commit()
                # update count for fixed topic
                try:
                    # update amount of sub-topics for for parent topic
                    parent_id = topic.parent_id
                    parent_topic = Topic.query.filter_by(id=parent_id).first()
                    parent_topic.count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                    pass
                # update topic created count for user
                try:
                    user = User.query.filter_by(id= topic.user_id).first()
                    user.topic_created_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())

                return send_result(message='Topic was created successfully.',
                                   data=marshal(topic, TopicDto.model_topic_response))
            else:  # topic already exist
                return send_error(message='The topic with name {} and parent topic id {} already exist'.format(data['name'], data['parent_id']))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create topic, please try again!')


    def get(self, args):
        try:
            if not isinstance(args, dict):
                return send_error(message='Could not parse the params')
            name, user_id, parent_id, is_fixed = None, None, None, None
            current_user, _ = AuthController.get_logged_user(request)
            if 'name' in args:
                name = args['name']
            if 'user_id' in args:
                try:
                    user_id = int(args['user_id'])
                except Exception as e:
                    print(e.__str__())
            if 'parent_id' in args:
                try:
                    parent_id = int(args['parent_id'])
                except Exception as e:
                    print(e.__str__())
            if 'is_fixed' in args:
                try:
                    is_fixed = int(args['is_fixed'])
                except Exception as e:
                    print(e.__str__())
                    
            query = db.session.query(Topic)
            is_filter = False
            if name is not None and not str(name).strip().__eq__(''):
                name = '%' + name.strip() + '%'
                query = query.filter(Topic.name.like(name))
            if user_id is not None:
                query = query.filter(Topic.user_id == user_id)
            if parent_id is not None:
                query = query.filter(Topic.parent_id == parent_id)
            if is_fixed is not None:
                query = query.filter(Topic.is_fixed == is_fixed)

            topics = query.order_by(desc(func.field(Topic.name, "Những lĩnh vực khác")))
            results = []
            for topic in topics:
                result = topic._asdict()
                # get user info
                result['parent'] = topic.parent
                result['children'] = topic.children
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == current_user.id,
                                                    TopicBookmark.topic_id == topic.id).first()
                    result['is_bookmarked_by_me'] = True if bookmark else False
                results.append(result)
            return send_result(marshal(results, TopicDto.model_topic_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load topics. Contact your administrator for solution.")


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Topic ID is null")
        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        if topic is None:
            return send_error(message="Could not find topic by this ID {}".format(object_id))
        current_user, _ = AuthController.get_logged_user(request)
        result = topic._asdict()
        # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
        if current_user:
            bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == current_user.id,
                                            TopicBookmark.topic_id == topic.id).first()
            result['is_bookmarked_by_me'] = True if bookmark else False
        return send_result(data=marshal(result, TopicDto.model_topic_response), message='Success')

    def get_sub_topics(self, object_id):
        if object_id is None:
            return send_error(message='Please give the topic ID.')
        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        if topic is None:
            return send_result(message='Could not find any topic.')
        if topic.is_fixed:
            id = topic.id
            result = topic.__dict__
            sub_topics = Topic.query.filter_by(parent_id=id).all()
            result['sub_topics'] = sub_topics
            return send_result(data=marshal(result, TopicDto.model_topic_response), message='Success')
        else:
            return send_result(
                message='The topic with the ID {} does not contain any sub-topics (Hint: send the ID of the fixed topic.')

    def update(self, object_id, data):
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message='Topic with the ID {} not found.'.format(object_id))
            elif topic.is_fixed:
                return send_error(message='Could not update for fixed topic.')
            else:
                topic = self._parse_topic(data=data, topic=topic)
                is_sensitive = check_sensitive(topic.name)
                if is_sensitive:
                    return send_error(message='Nội dung chủ đề mới tạo không hợp lệ.')

                # capitalize first letter
                topic.name = topic.name.capitalize()
                db.session.commit()
                current_user, _ = AuthController.get_logged_user(request)
                result = topic._asdict()
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == current_user.id,
                                                    TopicBookmark.topic_id == topic.id).first()
                    result['is_bookmarked_by_me'] = True if bookmark else False
                return send_result(message='Update successfully', data=marshal(result, TopicDto.model_topic_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update topic.')

    def delete(self, object_id):
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message="Topic with ID {} not found".format(object_id))
            else:
                db.session.delete(topic)
                db.session.commit()
                return send_result(message='Topic was deleted.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user with ID {}'.format(object_id))

    def create_endorsed_users(self, object_id, data):
        try:
            if not 'user_id' in data:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('user_id'))
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Topic', object_id))
            current_user, _ = AuthController.get_logged_user(request)
            user_id = data['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return send_error(message=messages.MSG_NOT_FOUND.format('User'))

            endorse = TopicUserEndorse()
            endorse.user_id = current_user.id
            endorse.endorsed_id = user.id
            endorse.topic_id = topic.id
            db.session.merge(endorse)
            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Topic'))
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_UPDATE_FAILED.format('Topic', e.__str__))

    def get_endorsed_users(self, object_id, args):
        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Topic', object_id))
            current_user, _ = AuthController.get_logged_user(request)
            query = topic.endorsed_users.paginate(page, per_page, error_out=True)
            res, code = paginated_result(query)
            results = []
            for user in res.get('data'):
                result = user._asdict()
                if current_user:
                    follow = UserFollow.query.filter(UserFollow.follower_id == current_user.id,
                                                    UserFollow.followed_id == user.id).first()
                    result['is_followed_by_me'] = True if follow else False
                results.append(result)
            res['data'] = marshal(results, TopicDto.model_endorsed_user)
            return res, code
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_GET_FAILED.format('Topic', e.__str__))

    def get_bookmarked_users(self, object_id, args):
        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Topic', object_id))
            current_user, _ = AuthController.get_logged_user(request)
            query = topic.bookmarked_users.paginate(page, per_page, error_out=True)
            res, code = paginated_result(query)
            results = []
            for user in res.get('data'):
                result = user._asdict()
                if current_user:
                    follow = UserFollow.query.filter(UserFollow.follower_id == current_user.id,
                                                    UserFollow.followed_id == user.id).first()
                    result['is_followed_by_me'] = True if follow else False
                results.append(result)
            res['data'] = marshal(results, TopicDto.model_endorsed_user)
            return res, code
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_GET_FAILED.format('Topic', e.__str__))


    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.MSG_PLEASE_PROVIDE.format("Topic ID"))
        if 'file' not in request.files:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('file'))

        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        if topic is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('topic', object_id))
        media_file = request.files.get('file', None)
        if not media_file:
            return send_error(message=messages.MSG_NO_FILE)
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            bucket = 'hoovada'
            sub_folder = 'topic' + '/' + encode_file_name(str(topic.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.MSG_ISSUE.format('Could not save your media file.'))

            topic.file_url = url
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Answer media'), data=marshal(topic, TopicDto.model_topic_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Topic media', e))

    def update_slug(self):
        topics = Topic.query.all()
        try:
            for topic in topics:
                if topic.parent:
                    topic.slug = '{}-{}'.format(slugify(topic.parent.name),slugify(topic.name))
                else:
                    topic.slug = '{}'.format(slugify(topic.name))
                db.session.commit()
            return send_result(marshal(topics, TopicDto.model_topic_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

    def _parse_topic(self, data, topic=None):
        if topic is None:
            topic = Topic()
        if 'parent_id' in data:
            try:
                topic.parent_id = int(data['parent_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'name' in data:
            topic.name = data['name']
            
        if 'count' in data:
            try:
                topic.count = int(data['count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            try:
                topic.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_count' in data:
            try:
                topic.question_count = int(data['question_count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_count' in data:
            try:
                topic.user_count = int(data['user_count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_count' in data:
            try:
                topic.answer_count = int(data['answer_count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'is_fixed' in data:  # we do not parse the value of is_fixed, because the fixed topics already passed
            pass
            # try:
            #     topic.is_fixed = bool(data['is_fixed'])
            # except Exception as e:
            #     print(e.__str__())
            #     pass
        topic.is_fixed = False
        if 'created_date' in data:
            try:
                topic.created_date = dateutil.parser.isoparse(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'description' in data:
            topic.description = data['description']

        if 'color_code' in data:
            topic.color_code = data['color_code']

        if 'is_nsfw' in data:  
            pass
            try:
                topic.is_nsfw = bool(data['is_nsfw'])
            except Exception as e:
                print(e.__str__())
                pass

        return topic

    def get_topic_hot(self,args):
        page = 1
        page_size = 20

        if args.get('page') and args['page'] > 0 :
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

        #query = db.session.query(Topic).order_by(desc(text("(SELECT COUNT(*) FROM `question_topic` WHERE topic_id = topic.id) + (SELECT COUNT(*) FROM `topic_article` WHERE topic_id = topic.id)")))
        query = db.session.query(Topic)
        query = query.join(QuestionTopic).outerjoin(ArticleTopic).group_by(Topic).order_by(desc(func.count(QuestionTopic.question_id) + func.count(ArticleTopic.article_id)))
        query.filter(Topic.is_fixed!=1)
        topics = query.offset(page * page_size).limit(page_size).all()

        if topics is not None and len(topics) > 0:
            return send_result(data=marshal(topics, TopicDto.model_topic_response),
                    message='Success')
        else:
            return send_result(message='Could not find any topics')
