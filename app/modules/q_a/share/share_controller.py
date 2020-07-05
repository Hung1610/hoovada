from datetime import datetime
import dateutil.parser
from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.question.question import Question
from app.modules.q_a.share.share import Share
from app.modules.q_a.share.share_dto import ShareDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result


class ShareController(Controller):
    def search(self, args):
        if not isinstance(args, dict):
            return send_error(message='Arguments must in dictionary form.')
        user_id, question_id, answer_id, from_date, to_date, facebook, twitter, zalo, anonymous = None, None, None, None, None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                pass
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                pass
        if 'answer_id' in args:
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                pass
        if 'from_date' in args:
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'facebook' in args:
            try:
                facebook = bool(args['facebook'])
            except Exception as e:
                pass
        if 'twitter' in args:
            try:
                twitter = bool(args['twitter'])
            except Exception as e:
                pass
        if 'zalo' in args:
            try:
                zalo = bool(args['zalo'])
            except Exception as e:
                pass
        if 'anonymous' in args:
            try:
                anonymous = bool(args['anonymous'])
            except Exception as e:
                pass
        if user_id is None and question_id is None and answer_id is None and from_date is None and to_date is None and facebook is None and twitter is None and zalo is None and anonymous is None:
            return send_error(message='Please give params to search.')
        query = db.session.query(Share)
        is_filter = False
        if user_id is not None:
            query = query.filter(Share.user_id == user_id)
            is_filter = True
        if question_id is not None:
            query = query.filter(Share.question_id == question_id)
            is_filter = True
        if answer_id is not None:
            query = query.filter(Share.answer_id == answer_id)
            is_filter = True
        if from_date is not None:
            query = query.filter(Share.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Share.created_date <= to_date)
            is_filter = True
        if facebook is not None:
            query = query.filter(Share.facebook == facebook)
            is_filter = True
        if twitter is not None:
            query = query.filter(Share.twitter == twitter)
            is_filter = True
        if zalo is not None:
            query = query.filter(Share.zalo == zalo)
            is_filter = True
        if anonymous is not None:
            query = query.filter(Share.anonymous == anonymous)
            is_filter = True
        if is_filter:
            shares = query.all()
            if len(shares) > 0:
                return send_result(data=marshal(shares, ShareDto.model_response), message='Success')
            else:
                return send_result('Could not find any result.')
        else:
            return send_result(message='Please give params to search.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error()
        if not 'user_id' in data:
            return send_error()
        if not 'question_id' in data and not 'answer_id' in data:
            return send_error(message='At least question_id or answer_id must be included in payload.')
        try:
            share = self._parse_share(data=data, share=None)
            if share.question_id and share.answer_id:
                return send_result(message='Stop hacking our website.')
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                user = User.query.filter_by(id=share.user_id).first()
                if share.question_id:
                    user.question_share_count += 1
                    question = Question.query.filter_by(id=share.question_id).first()
                    user_voted = User.query.filter_by(id=question.user_id).first()
                    user_voted.question_shared_count += 1
                if share.answer_id:
                    user.answer_share_count += 1
                    answer = Answer.query.filter_by(id=share.answer_id).first()
                    user_voted = User.query.filter_by(id=answer.user_id).first()
                    user_voted.answer_shared_count += 1
                db.session.commit()
            except Exception as e:
                pass
            return send_result()
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create share')

    def get(self):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data, share=None):
        if share is None:
            share = Share()
        if 'user_id' in data:
            try:
                share.user_id = int(data['user_id'])
            except Exception as e:
                pass
        if 'question_id' in data:
            try:
                share.question_id = int(data['question_id'])
            except Exception as e:
                pass
        if 'answer_id' in data:
            try:
                share.answer_id = int(data['answer_id'])
            except Exception as e:
                pass
        if 'facebook' in data:
            try:
                share.facebook = bool(data['facebook'])
            except Exception as e:
                pass
        if 'twitter' in data:
            try:
                share.twitter = bool(data['twitter'])
            except Exception as e:
                pass
        if 'linkedin' in data:
            try:
                share.linkedin = bool(data['linkedin'])
            except Exception as e:
                pass
        if 'zalo' in data:
            try:
                share.zalo = bool(data['zalo'])
            except Exception as e:
                pass
        if 'vkontakte' in data:
            try:
                share.vkontakte = bool(data['vkontakte'])
            except Exception as e:
                pass
        if 'anonymous' in data:
            try:
                share.anonymous = bool(data['anonymous'])
            except Exception as e:
                pass
        if 'mail' in data:
            try:
                share.mail = bool(data['mail'])
            except Exception as e:
                pass
        if 'link_copied' in data:
            try:
                share.link_copied = bool(data['link_copied'])
            except Exception as e:
                pass
        return share
