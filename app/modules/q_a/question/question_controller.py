import json
from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.question.question import Question
from app.modules.q_a.question.question_dto import QuestionDto
from app.utils.response import send_error, send_result


class QuestionController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form")
        if not 'title' in data:
            return send_error(message='Question must contain at least the title.')
        try:
            question = Question.query.filter_by(name=data['title']).first()
            if not question:  # the topic does not exist
                question = self._parse_question(data=data, question=None)
                db.session.add(question)
                db.session.commit()
                return send_result(message='Topic was created successfully.', data=marshal(question, QuestionDto.model))
            else:  # topic already exist
                return send_error(message='The question with title {} already exist'.format(data['title']))
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
        question = Question.query.filter_by(question_id=object_id).first()
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
            question = Question.query.filter_by(question_id=object_id).first()
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
            question = Question.query.filter_by(question_id=object_id).first()
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
            question.user_id = data['user_id']
        if '_question' in data:
            question._question = data['_question']
        if '_markdown' in data:
            question._markdown = data['_markdown']
        if '_html' in data:
            question._html = data['_html']

        if 'created_date' in data:
            try:
                question.created_date = datetime.fromisoformat(data['created_date'])
            except Exception as e:
                pass

        if 'updated_date' in data:
            try:
                question.updated_date = datetime.fromisoformat(data['updated_date'])
            except Exception as e:
                pass

        if 'views' in data:
            try:
                question.views = int(data['views'])
            except Exception as e:
                pass
        if 'last_activity' in data:
            try:
                question.last_activity = datetime.fromisoformat(data['last_activity'])
            except Exception as e:
                pass
        if 'answers_allowed' in data:
            try:
                question.answers_allowed = int(data['answers_allowed'])
            except Exception as e:
                pass
        if 'accepted_answer_id' in data:
            try:
                question.accepted_answer_id = int(data['accepted_answer_id'])
            except Exception as e:
                pass
        if 'anonymous' in data:
            try:
                question.anonymous = bool(data['anonymous'])
            except Exception as e:
                pass
        if 'image_ids' in data:
            try:
                question.image_ids = json.loads(data['image_ids'])
            except Exception as e:
                pass
        return question
