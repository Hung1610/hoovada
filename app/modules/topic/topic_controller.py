from flask_restx import marshal
import dateutil.parser

from app.modules.common.controller import Controller
from .topic import Topic
from .topic_dto import TopicDto
from app import db
from app.utils.response import send_error, send_result


class TopicController(Controller):

    def create_topics(self):
        fixed_topics = ["Du lịch", "Gia đình & Quan hệ xã hội", "Giáo dục & Tham khảo", "Giải trí & Âm nhạc",
                        "Khoa học Tự nhiên", "Khoa học Xã hội", "Kinh doanh & Tài chính", "Máy tính & Internet",
                        "Môi trường", "Nhà & Vườn", "Nơi ăn uống", "Sản phẩm của Yahoo", "Sức khỏe",
                        "Thai nghén & Nuôi dạy con", "Thể thao", "Thủ tục hành chính", "Tin tức & Sự kiện",
                        "Trò chơi & Giải trí", "Văn hóa & Xã hội", "Văn học & Nhân văn", "Vật nuôi",
                        "Vẻ đẹp & Phong cách", "Ô-tô & Vận tải", "Điện tử tiêu dùng", "Ẩm thực"]
        try:
            for topic_name in fixed_topics:
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
        if is_filter:
            topics = query.all()
            if topics is not None and len(topics) > 0:
                return send_result(marshal(topics, TopicDto.model), message='Success')
            else:
                return send_error(message='Could not find any topics.')
        else:
            return send_error(message='Could not find topics with these parameters.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        if not 'name' in data:
            return send_error(message='Topic name must be filled')
        if not 'parent_id' in data:
            return send_error(message='Topic must have a parent topic.')
        try:
            topic = Topic.query.filter(Topic.name == data['name'], Topic.parent_id == data['parent_id']).first()
            if not topic:  # the topic does not exist
                topic = self._parse_topic(data=data, topic=None)
                db.session.add(topic)
                db.session.commit()
                return send_result(message='Topic was created successfully.', data=marshal(topic, TopicDto.model))
            else:  # topic already exist
                return send_error(message='The topic with name {} already exist'.format(data['name']))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Coult not create topic. Contact administrator for solution.')

    def get(self):
        try:
            topics = Topic.query.all()
            return send_result(data=marshal(topics, TopicDto.model), message='Success')
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
            return send_result(data=marshal(topic, TopicDto.model), message='Success')

    def update(self, object_id, data):
        try:
            topic = Topic.query.filter_by(id=object_id).first()
            if not topic:
                return send_error(message='Topic with the ID {} not found.'.format(object_id))
            else:
                topic = self._parse_topic(data=data, topic=topic)
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(topic, TopicDto.model))
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
        if 'is_fixed' in data:
            try:
                topic.is_fixed = bool(data['is_fixed'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'created_date' in data:
            try:
                topic.created_date = dateutil.parser.isoparse(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass
        return topic
