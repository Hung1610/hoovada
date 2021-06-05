#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g, request
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func, text

# own modules
from common.db import db
from app.constants import messages
from app.modules.topic.topic_dto import TopicDto
from common.controllers.controller import Controller
from common.utils.file_handler import get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
from common.utils.util import encode_file_name
from common.utils.wasabi import upload_file
from app.modules.topic.bookmark.bookmark_controller import TopicBookmarkController
from common.es import get_model
from common.utils.util import strip_tags
from elasticsearch_dsl import Q

ESTopic = get_model('Topic')

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
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'name' in data or data['name'] == "":
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('topic name'))

        data['name'] = data['name'].strip().capitalize()

        if not 'parent_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('parent_id'))

        # check topic already exists
        topic = Topic.query.filter(Topic.name == data['name']).first()
        if topic is not None:
            return send_error(message='The topic with name {} already exist'.format(data['name']))
        
        current_user = g.current_user
        data['user_id'] = current_user.id
        try:
            topic = self._parse_topic(data=data, topic=None)
            topic.created_date = datetime.today()
            db.session.add(topic)
            db.session.flush()

            topic_dsl = ESTopic(_id=topic.id, description=topic.description, user_id=topic.user_id, name=topic.name, slug=topic.slug, is_fixed=0, created_date=topic.created_date)
            topic_dsl.save()
            db.session.commit()

            controller = TopicBookmarkController()
            controller.create(topic_id=topic.id)
            
            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(topic, TopicDto.model_topic_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_query(self):
        return self.get_model_class().query.order_by(desc(func.field(Topic.name, "Những lĩnh vực khác")))


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('topic_ids') and params.get('topic_ids') != '': 
            query = query.filter(Topic.id.in_(params.get('topic_ids')))

        if params.get('hot'):
            query = query.order_by(desc(text("article_count + question_count")))
        return query


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            """
            topics = res.get('data')
            results = []
            for topic in topics:
                result = topic._asdict()
                result['parent'] = topic.parent
                result['children'] = topic.children
                results.append(result)
            """
            res['data'] = marshal(results, TopicDto.model_topic_response)
            return paginated_result(query=query)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count})
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()

            if topic is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            return send_result(data=marshal(topic, TopicDto.model_topic_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_sub_topics(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()

        if topic is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        if topic.is_fixed:
            id = topic.id
            result = topic._asdict()
            sub_topics = Topic.query.filter_by(parent_id=id).all()
            result['sub_topics'] = sub_topics
            return send_result(data=marshal(result, TopicDto.model_topic_response))
        else:
            return send_error(message=messages.ERR_NOT_FOUND)


    def update(self, object_id, data):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        
        if not topic:
            return send_error(message=messages.ERR_NOT_FOUND)

        if 'name' in data:
            data['name'].strip().capitalize()


        try:
            topic = self._parse_topic(data=data, topic=topic)
            topic_dsl = ESTopic(_id=topic.id)
            topic_dsl.update(description=topic.description, name=topic.name, slug=topic.slug)
            db.session.commit()

            current_user = g.current_user 
            result = topic._asdict()
            bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == current_user.id, TopicBookmark.topic_id == topic.id).first()
            result['is_bookmarked_by_me'] = True if bookmark else False

            return send_result(data=marshal(result, TopicDto.model_topic_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()

            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND)

            Reputation.query.filter(Reputation.topic_id == topic.id).delete(synchronize_session=False)
            db.session.delete(topic)
            topic_dsl = ESTopic(_id=topic.id)
            topic_dsl.delete()
            db.session.commit()
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def create_endorsed_users(self, object_id, data):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        try:
            if not 'user_id' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND)

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
            return send_result(data=marshal(endorse.endorsed, TopicDto.model_user))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def delete_endorsed_users(self, object_id, user_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND)

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
                return send_error(message=messages.ERR_NOT_FOUND)

            db.session.delete(endorse)
            db.session.commit()
            return send_result()

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_endorsed_users(self, object_id, args):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND)

            g.endorsed_topic_id = object_id
            user_ids = [user.id for user in topic.endorsed_users]
            query = User.query.filter(User.id.in_(user_ids)).paginate(page, per_page, error_out=False)
            res, code = paginated_result(query)
            results = []
            for user in res.get('data'):
                result = user._asdict()
                results.append(result)
            res['data'] = marshal(results, TopicDto.model_user)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_bookmarked_users(self, object_id, args):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
            
        page, per_page = args.get('page', 1), args.get('per_page', 10)
        try:
            if object_id.isdigit():
                topic = Topic.query.filter_by(id=object_id).first()
            else:
                topic = Topic.query.filter_by(slug=object_id).first()
            
            if not topic:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            current_user = g.current_user 
            query = topic.bookmarked_users.paginate(page, per_page, error_out=False)
            res, code = paginated_result(query)
            
            results = []
            for user in res.get('data'):
                result = user._asdict()
                if current_user is not None:
                    follow = UserFollow.query.filter(UserFollow.follower_id == current_user.id, UserFollow.followed_id == user.id).first()
                    result['is_followed_by_me'] = True if follow else False
                results.append(result)
            
            res['data'] = marshal(results, TopicDto.model_user)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("id"))

        if 'file' not in request.files:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))

        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()

        if topic is None:
            return send_error(message=messages.ERR_NOT_FOUND)

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
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_recommended_users(self, object_id, args):
        '''Main logic for API GET /topic/recommended-users'''

        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("id"))

        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)


        if object_id.isdigit():
            topic = Topic.query.filter_by(id=object_id).first()
        else:
            topic = Topic.query.filter_by(slug=object_id).first()
        
        if topic is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        limit = args.get('limit', 10)
        try:
            total_score = db.func.sum(Reputation.score).label('total_score')

            top_users_reputation = Reputation.query.with_entities(
                    User,
                    total_score,
                )\
                .join(Reputation.user)\
                .filter(Reputation.topic_id == topic.id)\
                .group_by(User)\
                .having(total_score > 0)\
                .order_by(desc(total_score))\
                .limit(limit).all()
            results = [{'user': user._asdict(), 'total_score': total_score} for user, total_score in top_users_reputation]

            return send_result(data=marshal(results, TopicDto.model_recommended_users_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_recommended_topics(self, args):
        try:
            size = 20
            if 'size' in args:
                size = int(args['limit'])
            if not 'title' in args:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))
            s = ESTopic.search()
            q = Q("multi_match", query=args['title'], fields=['name'])
            s = s.query(q)
            s = s[0:size + 1]
            response = s.execute()
            hits = response.hits
            topics = []
            for h in hits:
                topic = db.session.query(Topic).filter_by(id=h.meta.id).first()
                if topic is not None and topic.is_fixed == 0:
                    topics.append(topic)
            return send_result(data=marshal(topics, TopicDto.model_topic_response), message=messages.MSG_GET_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


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
            try:
                topic.name = data['name']
            except Exception as e:
                print(e.__str__())
                pass
        
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
            try:
                topic.description = data['description']
            except Exception as e:
                print(e.__str__())
                pass

        if 'is_nsfw' in data: 
            pass
            try:
                topic.is_nsfw = bool(data['is_nsfw'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'file_url' in data: 
            pass
            try:
                topic.file_url = data['file_url']
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


    def update_slug(self):
        topics = Topic.query.all()
        try:
            for topic in topics:
                topic.slug = '{}'.format(slugify(topic.name))
                db.session.commit()
            return send_result(marshal(topics, TopicDto.model_topic_response), message='Success')
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))