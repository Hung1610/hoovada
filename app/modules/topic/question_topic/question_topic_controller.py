from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.topic.question_topic.question_topic import QuestionTopic
from app.modules.topic.question_topic.question_topic_dto import QuestionTopicDto
from app.modules.topic.topic import Topic
from app.utils.response import send_error, send_result


class QuestionTopicController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary type.')
        try:
            question_id = data['question_id']
            topic_id = data['topic_id']
            question_topic = QuestionTopic.query.filter(QuestionTopic.question_id == question_id,
                                                        QuestionTopic.topic_id == topic_id).first()
            if question_topic is not None:
                return send_error(message='This record already exist in database.')
            else:
                question_topic = self._parse_question_topic(data, None)
                question_topic.created_date = datetime.utcnow()
                db.session.add(question_topic)
                db.session.commit()

                # update question_count for topic
                try:
                    topic = Topic.query.filter_by(id=question_topic.topic_id).firs()
                    topic.question_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                    pass
                return send_result(data=marshal(question_topic, QuestionTopicDto.model), message='Create successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e.__str__())

    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Could not parse your parameters.')
        question_id, topic_id = None, None
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in args:
            try:
                topic_id = int(args['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if question_id is None and topic_id is None:
            return send_error(message='Please provide params to search')
        query = db.session.query(QuestionTopic)
        is_filter = False
        if question_id is not None:
            query = query.filter(QuestionTopic.question_id == question_id)
            is_filter = True
        if topic_id is not None:
            query = query.filter(QuestionTopic.topic_id == topic_id)
            is_filter = True
        if is_filter:
            question_topics = query.all()
            if question_topics is not None and len(question_topics) > 0:
                return send_result(data=marshal(question_topics, QuestionTopicDto.model), message='Success')
            else:
                return send_result(message='Not found.', code=201)
        else:
            return send_error(message='Could not find any records.')

    def get(self):
        try:
            question_topics = QuestionTopic.query.all()
            return send_result(data=marshal(question_topics, QuestionTopicDto.model), message='Success')
        except Exception as e:
            return send_error(message='Could not get list of question-topics')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Question-topic ID is null')
        question_topic = QuestionTopic.query.filter_by(id=object_id).first()
        if question_topic is None:
            return send_error(message='Could not find question-topic with the ID {}'.format(object_id))
        else:
            return send_result(data=marshal(question_topic, QuestionTopicDto.model), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='Question-topic ID is null')
        try:
            question_topic = QuestionTopic.query.filter_by(id=object_id).first()
            if question_topic is None:
                return send_error(message='Question-topic with the ID {} not found.'.format(object_id))
            else:
                question_topic = self._parse_question_topic(data=data, question_topic=question_topic)
                db.session.commit()
                return send_result(data=marshal(question_topic, QuestionTopicDto.model), message='Update Successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update question-topic')

    def delete(self, object_id):
        if object_id is None:
            return send_error(message="Question-topic ID is null")
        try:
            question_topic = QuestionTopic.query.filter_by(id=object_id).first()
            if question_topic is None:
                return send_error(message='Question-topic with the ID {} not found.'.format(object_id))
            else:
                db.session.delete(question_topic)
                db.session.commit()
                return send_result(message='Deleted Successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete question-topic')

    def _parse_question_topic(self, data, question_topic=None):
        if question_topic is None:
            question_topic = QuestionTopic()
        if 'question_id' in data:
            try:
                question_topic.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'topic_id' in data:
            try:
                question_topic.topic_id = int(data['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return question_topic
