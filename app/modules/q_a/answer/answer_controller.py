import json
from datetime import datetime
import dateutil.parser

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.question.question import Question
from app.modules.user.user import User
from app.utils.response import send_error, send_result


class AnswerController(Controller):

    def search(self, args):
        '''
        Search answers.

        :param args:

        :return:
        '''
        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        user_id, question_id, from_date, to_date = None, None, None, None  # , None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'created_date' in args:
        #     try:
        #         created_date = datetime.fromisoformat(args['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'updated_date' in args:
        #     try:
        #         updated_date = datetime.fromisoformat(args['updated_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
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

        if user_id is None and question_id is None and from_date is None and to_date is None:
            send_error(message='Provide params to search.')
        query = db.session.query(Answer)
        is_filter = False
        if user_id is not None:
            query = query.filter(Answer.user_id == user_id)
            is_filter = True
        if question_id is not None:
            query = query.filter(Answer.question_id == question_id)
            is_filter = True
        # if created_date is not None:
        #     query = query.filter(Answer.created_date == created_date)
        #     is_filter = True
        # if updated_date is not None:
        #     query = query.filter(Answer.updated_date == updated_date)
        #     is_filter = True
        if from_date is not None:
            query = query.filter(Answer.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Answer.created_date <= to_date)
            is_filter = True
        if is_filter:
            answers = query.all()
            if answers is not None and len(answers) > 0:
                # get user information for each answer.
                results = list()
                for answer in answers:
                    result = answer.__dict__
                    user = User.query.filter_by(id=answer.user_id).first()
                    result['user'] = user
                    results.append(result)
                return send_result(marshal(results, AnswerDto.model_response), message='Success')
            else:
                return send_result(message='Could not find any answers')
        else:
            return send_error(message='Could not find answers. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'question_id' in data:
            return send_error(message="Please fill the question ID")
        if not 'answer' in data:
            return send_error(message='Please fill the answer body before sending.')
        if not 'user_id' in data:
            return send_error(message='Please fill the user ID')
        try:
            # add new answer
            answer = self._parse_answer(data=data, answer=None)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message='The answer must include content.')
            answer.created_date = datetime.utcnow()
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.add(answer)
            db.session.commit()
            result = answer.__dict__
            # update answer_count cho user
            try:
                user = User.query.filter_by(id=answer.user_id).first()
                # update user information for answer
                result['user'] = user
                user.answer_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                pass

            # update answer count cho question
            try:
                question = Question.query.filter_by(id=answer.question_id).first()
                question.answers_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                pass
            # get user
            return send_result(message='Answer created successfully', data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create answer.')

    def get(self):
        '''
        [DEPRECATED]
        Hàm này được giữ lại, tuy nhiên sẽ không publish API, answers chỉ được nhận về qua search.
        :return:
        '''
        try:
            answers = Answer.query.limit(50).all()
            return send_result(data=marshal(answers, AnswerDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not load answers. Contact your administrator for solution.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Answer ID is null")
        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message='Could not find answer with the ID {}.'.format(object_id))
        else:
            # get user information for each answer.
            result = answer.__dict__
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            # return send_result(marshal(result, AnswerDto.model_response), message='Success')
            return send_result(data=marshal(result, AnswerDto.model_response), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message="Answer ID is null")
        if data is None or not isinstance(data, dict):
            return send_error(message="Data is null or not in dictionary form. Check again.")
        # if not 'question_id' in data:
        #     return send_error(message="Please fill the question ID")
        # if not 'answer' in data:
        #     return send_error(message='Please fill the answer body before sending.')
        # if not 'user_id' in data:
        #     return send_error(message='Please fill the user ID')
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message="Answer with the ID {} not found.".format(object_id))
            else:
                answer = self._parse_answer(data=data, answer=answer)
                if answer.answer.__str__().strip().__eq__(''):
                    return send_error(message='The answer must include content.')
                if answer.question_id is None:
                    return send_error(message='The question_id must be included.')
                if answer.user_id is None:
                    return send_error(message='The user_id must be included.')
                answer.updated_date = datetime.utcnow()
                answer.last_activity = datetime.utcnow()
                db.session.commit()
                # get user information for each answer.
                result = answer.__dict__
                user = User.query.filter_by(id=answer.user_id).first()
                result['user'] = user
                # return send_result(marshal(result, AnswerDto.model_response), message='Success')
                return send_result(message='Update successfully', data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not update answer.")

    def delete(self, object_id):
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message="Answer with ID {} not found.".format(object_id))
            else:
                # ------- delete from other tables---------#
                # delete from vote

                # delete from comment

                # delete from report

                # delete from share

                db.session.delete(answer)
                db.session.commit()
                return send_result(message="Answer with the ID {} was deleted.".format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not delete answer with ID {}.".format(object_id))

    def _parse_answer(self, data, answer=None):
        if answer is None:
            answer = Answer()
        # if 'created_date' in data:
        #     try:
        #         answer.created_date = dateutil.parser.isoparse(data['created_date'])
        #         # answer.created_date = datetime.fromisoformat(data['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'updated_date' in data:
        #     try:
        #         answer.updated_date = dateutil.parser.isoparse(data['updated_date']) #datetime.fromisoformat(data['update_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'last_activity' in data:
        #     try:
        #         answer.last_activity = dateutil.parser.isoparse(data['last_activity'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'upvote_count' in data:
        #     try:
        #         answer.upvote_count = int(data['upvote_count'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'downvote_count' in data:
        #     try:
        #         answer.downvote_count = int(data['downvote_count'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'anonymous' in data:
            try:
                answer.anonymous = bool(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'accepted' in data:
            try:
                answer.accepted = bool(data['accepted'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer' in data:
            answer.answer = data['answer']
        # if 'markdown' in data:
        #     answer.markdown = data['markdown']
        # if 'html' in data:
        #     answer.html = data['html']
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
        # if 'image_ids' in data:
        #     try:
        #         answer.image_ids = json.loads(data['image_ids'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'user_hidden' in data:
            try:
                answer.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                answer.user_hidden = False
                print(e.__str__())
                pass
        return answer
