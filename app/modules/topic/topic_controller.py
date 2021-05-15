#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from re import sub

# third-party modules
import dateutil.parser
from flask import current_app, g, request
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func, text

# own modules
from common.db import db
from app.constants import messages
from app.modules.topic.topic_dto import TopicDto
from common.controllers.controller import Controller
from common.utils.file_handler import append_id, get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
from common.utils.checker import check_spelling
from common.utils.sensitive_words import check_sensitive
from common.utils.util import encode_file_name
from common.utils.wasabi import upload_file
from app.modules.topic.bookmark.bookmark_controller import TopicBookmarkController
from common.es import get_model
from common.utils.util import strip_tags

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

User = db.get_model('User')
Topic = db.get_model('Topic')
TopicUserEndorse = db.get_model('TopicUserEndorse')
UserFollow = db.get_model('UserFollow')
Reputation = db.get_model('Reputation')
TopicBookmark = db.get_model('TopicBookmark')
ESTopic = get_model('Topic')

class TopicController(Controller):
    query_classname = 'Topic'
    special_filtering_fields = ['hot', 'topic_ids']
    allowed_ordering_fields = ['created_date', 'updated_date']
    
    def create_fixed_topics(self):
        fixed_topics = ["Những lĩnh vực khác", 
                        "Du lịch",
                        "Chính trị",
                        "Tôn giáo",
                        "Thể thao",
                        "Ẩm thực",
                        "Giáo dục & Việc làm",
                        "Sức khỏe",
                        "Văn học",
                        "Động vật",
                        "Ngôn ngữ",
                        "Âm nhạc & Điện ảnh",
                        "Nghệ thuật",
                        "Trò chơi & Giải trí",
                        "Nhà cửa & Xây dựng",
                        "Tài nguyên & Môi trường",
                        "Gia đình & Quan hệ xã hội",
                        "Khoa học tự nhiên",
                        "Khoa học xã hội và nhân văn",
                        "Đầu tư kinh doanh", 
                        "Công nghệ thông tin",
                        "Thai nghén & Nuôi dạy con",
                        "Luật pháp & Thủ tục", 
                        "Xe cộ & Giao thông",
                        "Mua sắm & Tiêu dùng",
                        "Văn hóa trong và ngoài nước",
                        "Điện tử & Máy móc",
                        "Con người & Tâm sinh lý",
                        "Hậu cần & Xuất nhập khẩu",
                        "Lịch sử & Truyền thuyết",
                        "Chuyện đời tư",
                        "Lĩnh vực người lớn",
                        "Truyền thông & Quảng cáo",
                        "Tiếng lóng & Biệt ngữ",
                        "hoovada.com"]

        try:
            admin_user = g.current_user
            for topic_name in fixed_topics:
                topic = Topic.query.filter(Topic.name == topic_name, Topic.is_fixed == True).first()
                if not topic:  # the topic does not exist
                    topic = Topic(name=topic_name, is_fixed=True, user_id=admin_user.id, color_code="#675DDA")
                    db.session.add(topic)
                    db.session.commit()
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create  fixed topic: {}'.format(str(e)))

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        
        if not 'name' in data or data['name'] == "":
            return send_error(message='Topic name must be filled!')
        else:
            topic_name = data['name']

            is_sensitive = check_sensitive(sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "",topic_name))
            if is_sensitive:
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

        if not 'parent_id' in data:
            return send_error(message='Topic must have a parent fixed_topic!')
        try:

            # only allowed Vietnamese or English topic names
            parent_topic = Topic.query.filter(Topic.id == data['parent_id']).first()
            if parent_topic is not None and parent_topic.name == 'Những lĩnh vực khác':
                spelling_errors = check_spelling(data['name'])
                if len(spelling_errors) > 0:
                    return send_error(message='Topic name is spelled wrongly!', data=spelling_errors)
           
            # check topic already exists
            topic = Topic.query.filter(Topic.name == data['name']).first()

            current_user = g.current_user
            data['user_id'] = current_user.id

            if not topic:  # the topic does not exist
                topic = self._parse_topic(data=data, topic=None)
                topic.created_date = datetime.today()

                # capitalize first letter
                topic.name = topic.name.capitalize()
                db.session.add(topic)
                db.session.flush()
                topic_dsl = ESTopic(_id=topic.id, description=topic.description, user_id=topic.user_id, name=topic.name, slug=topic.slug, is_fixed=0, created_date=topic.created_date)
                topic_dsl.save()
                db.session.commit()
                controller = TopicBookmarkController()
                controller.create(topic_id=topic.id)
                return send_result(message='Topic was created successfully.', data=marshal(topic, TopicDto.model_topic_response))
            
            else:  # topic already exist
                return send_error(message='The topic with name {} already exist'.format(data['name']))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create topic {}'.format(str(e)))


    def get_query(self):
        return self.get_model_class().query.order_by(desc(func.field(Topic.name, "Những lĩnh vực khác")))


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('topic_ids'):
            query = query.filter(Topic.id.in_(params.get('topic_ids')))

        if params.get('hot'):
            query = query.order_by(desc(text("article_count + question_count")))
        return query


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            current_user = g.current_user
            topics = res.get('data')
            results = []
            for topic in topics:
                result = topic._asdict()
                result['parent'] = topic.parent
                result['children'] = topic.children
                results.append(result)
            
            res['data'] = marshal(results, TopicDto.model_topic_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error('Could not load topics: {}'.format(str(e)))
    
    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count}, message='Success')
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
        return send_result(data=marshal(topic, TopicDto.model_topic_response), message='Success')


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
                message='The topic with the ID {} does not contain any sub-topics (Hint: send the ID of the fixed topic)')

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
                is_sensitive = check_sensitive(sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "",topic.name))
                if is_sensitive:
                    return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

                # capitalize first letter
                topic.name = topic.name.capitalize()
                topic_dsl = ESTopic(_id=topic.id)
                topic_dsl.update(description=topic.description, name=topic.name, slug=topic.slug)
                db.session.commit()

                current_user, _ = current_app.get_logged_user(request)
                result = topic._asdict()
                bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == current_user.id, TopicBookmark.topic_id == topic.id).first()
                result['is_bookmarked_by_me'] = True if bookmark else False
                return send_result(message='Update successfully', data=marshal(result, TopicDto.model_topic_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update topic: {}'.format(str(e)))


    def delete(self, object_id):
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message="Topic with ID {} not found".format(object_id))
            else:
                Reputation.query.filter(Reputation.topic_id == topic.id).delete(synchronize_session=False)
                db.session.delete(topic)
                topic_dsl = ESTopic(_id=topic.id)
                topic_dsl.delete()
                db.session.commit()
                return send_result(message='Topic was deleted.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user with ID {}'.format(object_id))

    def create_endorsed_users(self, object_id, data):
        try:
            if not 'user_id' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Topic', object_id))
            user_id = data['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return send_error(message=messages.ERR_NOT_FOUND)

            g.endorsed_topic_id = object_id
            current_user = g.current_user
            endorse = TopicUserEndorse.query.\
                filter(\
                    TopicUserEndorse.user_id == current_user.id,\
                    TopicUserEndorse.endorsed_id == user.id,\
                    TopicUserEndorse.topic_id == topic.id).\
                first()

            if not endorse:
                endorse = TopicUserEndorse()
                endorse.user_id = current_user.id
                endorse.endorsed_id = user.id
                endorse.topic_id = topic.id
                db.session.add(endorse)
                db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(endorse.endorsed, TopicDto.model_endorsed_user))
        except Exception as e:
            print(e)
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def delete_endorsed_users(self, object_id, user_id):
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Topic', object_id))
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return send_error(message=messages.ERR_NOT_FOUND)

            g.endorsed_topic_id = object_id
            current_user = g.current_user
            endorse = TopicUserEndorse.query.\
                filter(\
                    TopicUserEndorse.user_id == current_user.id,\
                    TopicUserEndorse.endorsed_id == user.id,\
                    TopicUserEndorse.topic_id == topic.id).\
                first()
            if not endorse:
                return send_error(message="Topic with ID {} not found".format(object_id))

            db.session.delete(endorse)
            db.session.commit()

            return send_result(message='TopicEndorse was deleted.')
        except Exception as e:
            print(e)
            return send_error(message=messages.ERR_DELETE_FAILED.format('TopicEndorse', e))

    def get_endorsed_users(self, object_id, args):
        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Topic', object_id))
            g.endorsed_topic_id = object_id
            user_ids = [user.id for user in topic.endorsed_users]
            query = User.query.filter(User.id.in_(user_ids)).paginate(page, per_page, error_out=False)
            res, code = paginated_result(query)
            results = []
            for user in res.get('data'):
                result = user._asdict()
                results.append(result)
            res['data'] = marshal(results, TopicDto.model_endorsed_user)
            return res, code
        except Exception as e:
            print(e)
            return send_error(message=messages.ERR_GET_FAILED.format('Topic', e))

    def get_bookmarked_users(self, object_id, args):
        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Topic', object_id))
            
            current_user, _ = current_app.get_logged_user(request)
            query = topic.bookmarked_users.paginate(page, per_page, error_out=False)
            res, code = paginated_result(query)
            results = []
            for user in res.get('data'):
                result = user._asdict()
                if current_user is not None:
                    follow = UserFollow.query.filter(UserFollow.follower_id == current_user.id, UserFollow.followed_id == user.id).first()
                    result['is_followed_by_me'] = True if follow else False
                results.append(result)
            
            res['data'] = marshal(results, TopicDto.model_endorsed_user)
            return res, code
        except Exception as e:
            print(e)
            return send_error(message=messages.ERR_GET_FAILED.format('Topic', e))

    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Topic ID"))
        if 'file' not in request.files:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))

        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        if topic is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('topic', object_id))
        media_file = request.files.get('file', None)
        if not media_file:
            return send_error(message=messages.ERR_NO_FILE)
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            sub_folder = 'topic' + '/' + encode_file_name(str(topic.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.ERR_ISSUE.format('Could not save your media file.'))

            topic.file_url = url
            db.session.commit()
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(topic, TopicDto.model_topic_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

    def update_slug(self):
        topics = Topic.query.all()
        try:
            for topic in topics:
                topic.slug = '{}'.format(slugify(topic.name))
                db.session.commit()
            return send_result(marshal(topics, TopicDto.model_topic_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

    def update_color(self):
        topics = Topic.query.filter(Topic.is_fixed == True).all()
        try:
            for topic in topics:
                topic.color_code = "#675DDA"
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
        
        if 'user_id' in data:
            try:
                topic.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        topic.is_fixed = False
        if 'created_date' in data:
            try:
                topic.created_date = dateutil.parser.isoparse(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'description' in data:
            topic.description = data['description']

        if 'is_nsfw' in data: 
            pass
            try:
                topic.is_nsfw = bool(data['is_nsfw'])
            except Exception as e:
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'color_code' in data:
                topic.color_code = data['color_code']
            if 'allow_follow' in data:
                try:
                    topic.allow_follow = bool(data['allow_follow'])
                except Exception as e:
                    print(e.__str__())
                    pass

        return topic
