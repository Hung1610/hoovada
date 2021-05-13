#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from app.modules.topic.topic_controller import UserFollow
from datetime import datetime

# third-party modules
from flask_restx import marshal

# own modules   
from common.db import db
from app.modules.user.reputation.reputation_dto import ReputationDto
from common.controllers.controller import Controller
from common.models import Reputation, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


Topic = db.get_model('Topic')

class ReputationController(Controller):

    def get(self, args):
        topic_id, user_id = None, None
        if 'topic_id' in args:
            try:
                topic_id = int(args['topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        query = Reputation.query
        if topic_id is not None:
            query = query.filter(Reputation.topic_id == topic_id)
        if user_id is not None:
            query = query.filter(Reputation.user_id == user_id)
        
        reputations = query.all()
        results = list()

        for reputation in reputations:
            user = reputation.user
            result = user._asdict()
            result['reputation'] = reputation._asdict()
            results.append(result)
        return send_result(marshal(results, ReputationDto.model_user_reputation_response), message='Success')

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
            return send_result(marshal(Reputation.query.all(), ReputationDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

    def create(self, data):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def get_by_id(self):
        pass
