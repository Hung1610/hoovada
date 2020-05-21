import json
from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.utils.response import send_error, send_result


class AnswerController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'question_id' in data:
            return send_error(message="Please fill the question ID")
        try:
            answer = self._parse_answer(data=data, answer=None)
            db.session.add(answer)
            db.session.commit()
            return send_result(message='Answer created successfully', data=marshal(answer, AnswerDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create answer.')

    def get(self):
        try:
            answers = Answer.query.all()
            return send_result(data=marshal(answers, AnswerDto.model), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not load answers. Contact your administrator for solution.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Answer ID is null")
        answer = Answer.query.filter_by(answer_id=object_id).first()
        if answer is None:
            return send_error(message='Could not find answer with the ID {}.'.format(object_id))
        else:
            return send_result(data=marshal(answer, AnswerDto.model), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message="Answer ID is null")
        if data is None or not isinstance(data, dict):
            return send_error(message="Data is null or not in dictionary form. Check again.")
        try:
            answer = Answer.query.filter_by(answer_id=object_id).first()
            if answer is None:
                return send_error(message="Answer with the ID {} not found.".format(object_id))
            else:
                answer = self._parse_answer(data=data, answer=answer)
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(answer, AnswerDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not update answer.")

    def delete(self, object_id):
        try:
            answer = Answer.query.filter_by(answer_id=object_id)
            if answer is None:
                return send_error(message="Answer with ID {} not found.".format(object_id))
            else:
                db.session.delete(answer)
                db.session.commit()
                return send_result(message="Answer with the ID {} was deleted.".format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not delete answer with ID {}.".format(object_id))

    def _parse_answer(self, data, answer=None):
        if answer is None:
            answer = Answer()
        if 'answer_id' in data:
            answer.answer_id = int(data['answer_id'])
        if 'created_date' in data:
            try:
                answer.created_date = datetime.fromisoformat(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'update_date' in data:
            try:
                answer.update_date = datetime.fromisoformat(data['update_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'last_activity' in data:
            try:
                answer.last_activity = datetime.fromisoformat(data['last_activity'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'upvote_count' in data:
            try:
                answer.upvote_count = int(data['upvote_count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'downvote_count' in data:
            try:
                answer.downvote_count = int(data['downvote_count'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'anonymous' in data:
            try:
                answer.anonymous = int(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'accepted' in data:
            try:
                answer.accepted = bool(data['accepted'])
            except Exception as e:
                print(e.__str__())
                pass
        if '_answer_body' in data:
            answer._answer_body = data['_answer_body']
        if '_markdown' in data:
            answer._markdown = data['_markdown']
        if '_html' in data:
            answer._html = data['_html']
        if 'user_id' in data:
            try:
                answer.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in data:
            try:
                answer.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'image_ids' in data:
            try:
                answer.image_ids = json.loads(data['image_ids'])
            except Exception as e:
                print(e.__str__())
                pass
        return answer
