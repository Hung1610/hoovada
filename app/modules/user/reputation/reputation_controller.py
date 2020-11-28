#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import marshal

# own modules   
from app.app import db
from app.modules.user.reputation.reputation_dto import ReputationDto
from common.controllers.controller import Controller
from common.models import Reputation, User
from common.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReputationController(Controller):

    def create(self, data):
        if not isinstance(data, dict):
            return
        if not 'user_id' in data:
            return
        if not 'topic_id' in data:
            return
        try:
            reputation = Reputation()
            reputation.user_id = data['user_id']
            reputation.topic_id = data['topic_id']
            reputation.score = 0
            reputation.created_date = datetime.utcnow()
            db.session.add(reputation)
            db.session.commit()
            return True
        except Exception as e:
            return False

    def get(self):
        pass

    def get_by_user_id(self, user_id):
        if user_id is None:
            return None
        reputation = Reputation.query.filter_by(user_id=user_id).first()
        return reputation

    def update(self, object_id, data):
        if object_id is None:
            return
        if not isinstance(data, dict):
            return
        try:
            user_id = data['user_id']
            topic_id = data['topic_id']
        except Exception as e:
            print(e.__str__())
            pass

    def update_all(self):
        reps = Reputation.query.all()
        try:
            for rep in reps:
                rep.updated_date = datetime.now
                db.session.commit()
            return send_result(marshal(reps, ReputationDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=e)

    def delete(self, object_id):
        pass

    def _parse_reputation(self, data, reputation=None):
        if reputation is None:
            reputation = Reputation()
        if 'user_id' in data:
            reputation.user_id = data['user_id']
        if 'topic_id' in data:
            reputation.topic_id = data['topic_id']

    def reputation_update(self, user_id, user_voted_id, topic_id):
        if user_id is None or not isinstance(user_id, int):
            return
        if user_voted_id is None or not isinstance(user_voted_id, int):
            return
        if topic_id is None or not isinstance(topic_id, int):
            return
        try:
            reputation = Reputation()
        except Exception as e:
            print(e.__str__())
            pass


    def get_by_id(self, user_id):
        pass

    def search(self, args):
            if not isinstance(args, dict):
                return send_error(message='Từ khoá truyền vào không đúng định dạng.')
            topic_id = None
            if 'topic_id' in args:
                try:
                    topic_id = int(args['topic_id'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if topic_id is None :
                return send_error(message='Vui lòng nhập từ khoá tìm kiếm.')
            query = db.session.query(Reputation)
            is_filter = False
            if topic_id is not None:
                query = query.filter(Reputation.topic_id == topic_id)
                is_filter = True
            if is_filter:
                reputations = query.all()
                if reputations is not None and len(reputations) > 0:
                    results = list()
                    for reputation in reputations:
                        # get user info
                        user = User.query.filter_by(id=reputation.user_id).first()
                        result = user.__dict__

                        result['reputation'] = reputation.__dict__
                        results.append(result)
                    return send_result(marshal(results, ReputationDto.user_reputation_response), message='Success')
                else:
                    return send_result(message='Không thể tìm thấy người dùng.')
            else:
                return send_error(message='Không thể tìm thấy người dùng. Vui lòng kiểm tra lại từ khoá tìm kiếm.')
