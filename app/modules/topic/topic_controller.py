#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import ast
from datetime import datetime

# third-party modules
from flask_restx import marshal
from flask import request
import dateutil.parser
from sqlalchemy import or_, and_, func, desc

# own modules
from app.modules.common.controller import Controller
from app.modules.auth.auth_controller import AuthController
from app.modules.topic.topic import Topic
from app.modules.topic.topic_dto import TopicDto
from app import db
from app.utils.response import send_error, send_result, send_paginated_result
from app.modules.user.user import User
from app.utils.sensitive_words import check_sensitive
from app.constants import messages

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
                and_(Topic.name == data['name'],Topic.name == data['name'], int(data['parent_id'])>0))
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


    def get(self):
        try:
            topics = Topic.query.filter_by(is_fixed=True).all()
            # results = list()
            # for topic in topics:
            #     id = topic.id
            #     result = topic.__dict__
            #     sub_topics = Topic.query.filter_by(parent_id=id).all()
            #     result['sub_topics'] = sub_topics
            #     results.append(result)
            # json_result = ast.literal_eval(results.__str__())
            return send_result(data=marshal(topics, TopicDto.model_topic_response),
                               message='Success')  # marshal(results, TopicDto.model_response)
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load topics. Contact your administrator for solution.")


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Topic ID is null")
        topic = Topic.query.filter_by(id=object_id).first()
        if topic is None:
            return send_error(message="Could not find topic by this ID {}".format(object_id))
        else:
            return send_result(data=marshal(topic, TopicDto.model_topic_response), message='Success')

    def get_sub_topics(self, fixed_topic_id):
        if fixed_topic_id is None:
            return send_error(message='Please give the topic ID.')
        topic = Topic.query.filter_by(id=fixed_topic_id).first()
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
            topic = Topic.query.filter_by(id=object_id).first()
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
                return send_result(message='Update successfully', data=marshal(topic, TopicDto.model_topic_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update topic.')

    def delete(self, object_id):
        try:
            topic = Topic.query.filter_by(id=object_id).first()
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
            if not 'user_ids' in data:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('user_ids'))
            topic = Topic.query.filter_by(id=object_id).first()
            if not topic:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Topic', object_id))
            current_user, _ = AuthController.get_logged_user(request)
            user_ids = data['user_ids']
            for user_id in user_ids:
                try:
                    user = User.query.filter_by(id=user_id).first()
                    if user:
                        topic.endorsed_users.append(user)
                except Exception as e:
                    print(e)
                    pass
            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Topic'))
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_UPDATE_FAILED.format('Topic', e.__str__))

    def get_endorsed_users(self, object_id, args):
        if not 'page' in args:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('page'))
        if not 'per_page' in args:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('per_page'))
        page, per_page = args.get('page', 0), args.get('per_page', 10)
        try:
            topic = Topic.query.filter_by(id=object_id).first()
            if not topic:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Topic', object_id))
            result = topic.endorsed_users.paginate(page, per_page, error_out=True)
            return send_paginated_result(message=messages.MSG_UPDATE_SUCCESS.format('Topic'), query=result, dto=TopicDto.model_endorsed_user)
        except Exception as e:
            print(e)
            return send_error(message=messages.MSG_UPDATE_FAILED.format('Topic', e.__str__))

    def _parse_topic(self, data, topic=None):
        if topic is None:
            topic = Topic()
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
        if 'parent_id' in data:
            try:
                topic.parent_id = int(data['parent_id'])
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

        return topic
