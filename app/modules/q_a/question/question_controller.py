import json
from datetime import datetime
import dateutil.parser

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.question.question import Question
from app.modules.q_a.question.question_dto import QuestionDto
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
            if questions is not None and len(questions)>0:
                return send_result(marshal(questions, QuestionDto.model), message='Success')
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
                question = self._parse_question(data=data, question=None)
                db.session.add(question)
                db.session.commit()
                return send_result(message='Topic was created successfully.', data=marshal(question, QuestionDto.model))
            else:  # topic already exist
                return send_error(message='You already created the question with title {}.'.format(data['title']))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create topic. Contact administrator for solution.')

    def get(self):
        try:
            questions = Question.query.all()
            return send_result(data=marshal(questions, QuestionDto.model), message='Success')
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
            return send_result(data=marshal(question, QuestionDto.model), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message="Question ID is null")
        if not isinstance(data, dict):
            return send_error(message="Data is not in dictionary form.")
        try:
            question = Question.query.filter_by(id=object_id).first()
            if question is None:
                return send_error(message="Question with the ID {} not found".format(object_id))
            else:
                question = self._parse_question(data=data, question=question)
                db.session.commit()
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
        if 'question' in data:
            question.question = data['question']
        if 'markdown' in data:
            question.markdown = data['markdown']
        if 'html' in data:
            question.html = data['html']

        if 'created_date' in data:
            try:
                question.created_date = dateutil.parser.isoparse(data['created_date'])
            except Exception as e:
                pass

        if 'updated_date' in data:
            try:
                question.updated_date = dateutil.parser.isoparse(data['updated_date'])
            except Exception as e:
                pass

        if 'views' in data:
            try:
                question.views = int(data['views'])
            except Exception as e:
                pass
        if 'last_activity' in data:
            try:
                question.last_activity = dateutil.parser.isoparse(data['last_activity'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answers_allowed' in data:
            try:
                question.answers_allowed = int(data['answers_allowed'])
            except Exception as e:
                print(e.__str__())
                pass
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
                pass
        if 'image_ids' in data:
            try:
                question.image_ids = json.loads(data['image_ids'])
            except Exception as e:
                print(e.__str__())
                pass
        return question
