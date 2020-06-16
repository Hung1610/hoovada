import json
from datetime import datetime
import dateutil.parser

from flask_restx import marshal
from sqlalchemy import desc

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.question.question import Question
from app.modules.q_a.question.question_dto import QuestionDto
from app.modules.topic.question_topic.question_topic import QuestionTopic
from app.modules.topic.topic import Topic
from app.utils.response import send_error, send_result


class QuestionController(Controller):

    def search(self, args):
        '''
        Search questions.

        :param args:
        :return:
        '''
        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        title, user_id, fixed_topic_id, created_date, updated_date, from_date, to_date, anonymous = None, None, None, None, None, None, None, None
        if 'title' in args:
            title = args['title']
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'fixed_topic_id' in args:
            try:
                fixed_topic_id = int(args['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'created_date' in args:
            try:
                created_date = datetime.fromisoformat(args['created_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'updated_date' in args:
            try:
                updated_date = datetime.fromisoformat(args['updated_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'from_date' in args:
            try:
                from_date = datetime.fromisoformat(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = datetime.fromisoformat(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'anonymous' in args:
            try:
                anonymous = int(args['anonymous'])
            except Exception as e:
                print(e.__str__())
                pass
        if title is None and user_id is None and fixed_topic_id is None and created_date is None and updated_date is None and anonymous is None:
            send_error(message='Provide params to search.')
        query = db.session.query(Question)
        is_filter = False
        if title is not None and not str(title).strip().__eq__(''):
            title = '%' + title.strip() + '%'
            query = query.filter(Question.title.like(title))
            is_filter = True
        if user_id is not None:
            query = query.filter(Question.user_id == user_id)
            is_filter = True
        if fixed_topic_id is not None:
            query = query.filter(Question.fixed_topic_id == fixed_topic_id)
            is_filter = True
        if created_date is not None:
            query = query.filter(Question.created_date == created_date)
            is_filter = True
        if updated_date is not None:
            query = query.filter(Question.updated_date == updated_date)
            is_filter = True
        if from_date is not None:
            query = query.filter(Question.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Question.created_date <= to_date)
            is_filter = True
        if is_filter:
            questions = query.all()
            if questions is not None and len(questions) > 0:
                results = list()
                for question in questions:
                    result = question.__dict__
                    # get all topics that question belongs to
                    question_id = question.id
                    question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
                    topics = list()
                    for question_topic in question_topics:
                        topic_id = question_topic.topic_id
                        topic = Topic.query.filter_by(id=topic_id).first()
                        topics.append(topic)
                    result['topics'] = topics
                    results.append(result)
                return send_result(marshal(results, QuestionDto.model_question_response), message='Success')
            else:
                return send_result(message='Could not find any questions')
        else:
            return send_error(message='Could not find questions. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form")
        if not 'title' in data:
            return send_error(message='Question must contain at least the title.')
        if not 'user_id' in data:
            return send_error(message='Question must contain user_id (included anonymous)')
        try:
            title = data['title']
            user_id = data['user_id']
            question = Question.query.filter(Question.title == title).filter(Question.user_id == user_id).first()
            if not question:  # the topic does not exist
                question, topic_ids = self._parse_question(data=data, question=None)
                question.created_date = datetime.utcnow()
                question.last_activity = datetime.utcnow()
                db.session.add(question)
                db.session.commit()
                # update question_count for topic
                fixed_topic_id = question.fixed_topic_id
                fixed_topic = Topic.query.filter_by(id=fixed_topic_id).first()
                fixed_topic.question_count += 1
                db.session.commit()
                result = question.__dict__
                # add question_topics
                question_id = question.id
                topics = list()
                for topic_id in topic_ids:
                    question_topic = QuestionTopic(question_id=question_id, topic_id=topic_id)
                    db.session.add(question_topic)
                    db.session.commit()
                    topic = Topic.query.filter_by(id=topic_id).first()
                    # update question_count for current topic.
                    topic.question_count += 1
                    db.session.commit()
                    topics.append(topic)
                result['topics'] = topics
                return send_result(message='Question was created successfully.',
                                   data=marshal(result, QuestionDto.model_question_response))
            else:  # topic already exist
                return send_error(message='You already created the question with title {}.'.format(data['title']))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could not create question. Contact administrator for solution.')

    def get(self):
        try:
            questions = Question.query.order_by(desc(Question.created_date)).limit(50).all()
            # for question in questions:
            #     # # chay cau lenh de cap nhat la fixed_topic_name
            #     # fixed_topic_id = question.fixed_topic_id
            #     # fixed_topic = Topic.query.filter_by(id=fixed_topic_id).first()
            #     # if fixed_topic:
            #     #     question.fixed_topic_name = fixed_topic.name
            #     # question.views_count = 0
            #     # question.answers_count = 0
            #     # question.upvote_count = 0
            #     # question.downvote_count = 0
            #     # question.favorite_count = 0
            #     # question.share_count = 0
            #
            #     # update anonymous va user_hidden
            #     if question.user_id == 6:
            #         question.anonymous = 1
            #     else:
            #         question.anonymous = 0
            #     question.user_hidden = 0
            # db.session.commit()
            results = list()
            for question in questions:
                result = question.__dict__
                # get all topics that question belongs to
                question_id = question.id
                question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
                topics = list()
                for question_topic in question_topics:
                    topic_id = question_topic.topic_id
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                result['topics'] = topics
                results.append(result)
            return send_result(data=marshal(results, QuestionDto.model_question_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load questions. Contact your administrator for solution.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Question ID is null")
        question = Question.query.filter_by(id=object_id).first()
        if question is None:
            return send_error(message='Could not find question with the ID {}'.format(object_id))
        else:
            result = question.__dict__
            # get all topics that question belongs to
            question_id = question.id
            question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
            topics = list()
            for question_topic in question_topics:
                topic_id = question_topic.topic_id
                topic = Topic.query.filter_by(id=topic_id).first()
                topics.append(topic)
            result['topics'] = topics
            return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')

    def update(self, object_id, data):
        '''
        Thuc hien update nhu sau:
        Khi nguoi dung lua chon thay the hoac xoa topic khoi question thi thuc hien cap nhat vao bang question_topic.
        :param object_id:
        :param data:
        :return:
        '''
        if object_id is None:
            return send_error(message="Question ID is null")
        if not isinstance(data, dict):
            return send_error(message="Data is not in dictionary form.")
        try:
            question = Question.query.filter_by(id=object_id).first()
            if question is None:
                return send_error(message="Question with the ID {} not found".format(object_id))
            else:
                question, _ = self._parse_question(data=data, question=question)
                # update topics to question_topic table
                question.updated_date = datetime.utcnow()
                question.last_activity = datetime.utcnow()
                db.session.commit()
                result = question.__dict__
                # get all topics that question belongs to
                question_id = question.id
                question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
                topics = list()
                for question_topic in question_topics:
                    topic_id = question_topic.topic_id
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                result['topics'] = topics
                return send_result(message="Update successfully", data=marshal(question, QuestionDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update question.')

    def delete(self, object_id):
        try:
            question = Question.query.filter_by(id=object_id).first()
            if question is None:
                return send_error(message="Question with ID {} not found".format(object_id))
            else:
                # delete from question_topic

                # delete from vote

                # delete from share

                # delete from answer

                # delete from timline

                # delete from

                db.session.delete(question)
                db.session.commit()
                return send_result(message="Question with the ID {} was deleted.".format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not delete question with ID {}".format(object_id))

    def _parse_question(self, data, question=None):
        if question is None:
            question = Question()
        question.title = data['title']
        if 'user_id' in data:
            try:
                question.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass
        if 'fixed_topic_id' in data:
            try:
                question.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'fixed_topic_name' in data:
            question.fixed_topic_name = data['fixed_topic_name']
        if 'question' in data:
            question.question = data['question']
        # if 'markdown' in data:
        #     question.markdown = data['markdown']
        # if 'html' in data:
        #     question.html = data['html']

        # if 'created_date' in data:
        #     try:
        #         question.created_date = dateutil.parser.isoparse(data['created_date'])
        #     except Exception as e:
        #         pass
        #
        # if 'updated_date' in data:
        #     try:
        #         question.updated_date = dateutil.parser.isoparse(data['updated_date'])
        #     except Exception as e:
        #         pass

        # if 'views' in data:
        #     try:
        #         question.views = int(data['views'])
        #     except Exception as e:
        #         pass
        # if 'last_activity' in data:
        #     try:
        #         question.last_activity = dateutil.parser.isoparse(data['last_activity'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'answers_count' in data:
        #     try:
        #         question.answers_count = int(data['answers_count'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'accepted_answer_id' in data:
            try:
                question.accepted_answer_id = int(data['accepted_answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'anonymous' in data:
            try:
                question.anonymous = bool(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                question.anonymous = False
        if 'user_hidden' in data:
            try:
                question.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                question.user_hidden = False
                print(e.__str__())
                pass
        # if 'image_ids' in data:
        #     try:
        #         question.image_ids = json.loads(data['image_ids'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        topic_ids = None
        if 'topic_ids' in data:
            try:
                topic_ids = data['topic_ids']
            except Exception as e:
                print(e.__str__())
                pass
        return question, topic_ids
