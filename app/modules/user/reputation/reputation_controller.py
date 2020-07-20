from datetime import datetime

from app import db
from app.modules.common.controller import Controller
from app.modules.user.reputation.reputation import Reputation


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
