#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from app.modules.topic.topic_controller import UserFollow
from datetime import datetime

# third-party modules
from flask_restx import marshal

# own modules   
from common.db import db
from app.constants import messages
from app.modules.user.reputation.reputation_dto import ReputationDto
from common.controllers.controller import Controller
from common.models import Reputation, User
from common.utils.response import paginated_result, send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Topic = db.get_model('Topic')
Answer = db.get_model('Answer')
class ReputationController(Controller):
    query_classname = 'Reputation'
    allowed_ordering_fields = ['created_date', 'updated_date', 'score']

    def is_answered_by_me(self):
        if g.current_user:
            answer = Answer.query.filter(Answer.user_id == g.current_user.id, Answer.question_id == self.id).first()
            return True if answer is not None else False
        return False

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            results = []
            for reputation in res['data']:
                user = reputation.user
                result = user._asdict()
                result['reputation'] = reputation._asdict()
                topic = reputation.topic
                answered_question_count = 0
                if topic is not None:
                    questions = topic.questions
                    for question in questions:
                        answer = Answer.query.filter(Answer.user_id == reputation.user_id, Answer.question_id == question.id).first()
                        if answer is not None:
                            answered_question_count += 1
                result['answered_question_count'] = answered_question_count
                results.append(result)

            res['data'] = marshal(results, ReputationDto.model_user_reputation_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))

            
    def update_all(self):
        users = User.query.all()
        topics = Topic.query.all()
        try:
            for user in users:
                for topic in topics:
                    reputation_creator = Reputation.query.filter(Reputation.user_id == user.id, \
                        Reputation.topic_id == topic.id).first()
                    if reputation_creator is None:
                        reputation_creator = Reputation()
                        reputation_creator.user_id = user.id
                        reputation_creator.topic_id = topic.id
                        db.session.add(reputation_creator)
                    reputation_creator.updated_date = datetime.now()
                    db.session.commit()
            return send_result(marshal(Reputation.query.all(), ReputationDto.model_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))

    def create(self, data):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def get_by_id(self):
        pass
