#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-part modules
import dateutil.parser
from flask_restx import marshal
from flask import request
from sqlalchemy import desc

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.question.question import Question
from app.modules.q_a.share.share import Share
from app.modules.q_a.share.share_dto import ShareDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result
from app.modules.auth.auth_controller import AuthController

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


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
            return send_error(message='Dữ liệu không đúng định dạng hoặc thiếu, vui lòng kiểm tra lại')
        user, message = AuthController.get_logged_user(request)

        #if not 'user_id' in data:
        #    return send_error()
        
        if not 'question_id' in data and not 'answer_id' in data:
            return send_error(message='Phải có ít nhất 1 câu hỏi hoặc 1 câu trả lời.')
        try:
            share = self._parse_share(data=data)
            if share.question_id and share.answer_id:
                return send_result(message='Stop hacking our website.')
            share.created_date = datetime.utcnow()
            db.session.add(share)
            db.session.commit()
            # update other values
            try:
                #user = User.query.filter_by(id=share.user_id).first()
                if share.question_id:
                    if user:
                        user.question_share_count += 1

                    question = Question.query.filter_by(id=share.question_id).first()
                    if not question:
                        return send_error(message='Không tìm thấy câu hỏi')
                    
                    user_voted = User.query.filter_by(id=question.user_id).first()
                    if not user_voted:
                        return send_error(message='Không tìm thấy chủ của câu hỏi')
                    user_voted.question_shared_count += 1
                
                if share.answer_id:
                    if user:
                        user.answer_share_count += 1
                    
                    answer = Answer.query.filter_by(id=share.answer_id).first()
                    if not answer:
                        return send_error(message='Không tìm thấy câu trả lời')

                    user_voted = User.query.filter_by(id=answer.user_id).first()
                    if not user_voted:
                        return send_error(message='Không tìm thấy tác giả câu trả lời')
                    user_voted.answer_shared_count += 1
                if user:
                    share.user_id = user.id
                db.session.commit()
            except Exception as e:
                pass
            return send_result()
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create share')

    def get_by_id(self):
        pass

    def get(self):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def _parse_share(self, data):
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

<<<<<<< HEAD
def get_share_by_user_id(self,args):
        """
        Search share.
=======
>>>>>>> dev

    def get_share_by_user_id(self,args):
        """ Search share.

<<<<<<< HEAD
        :return: List of shares  (questions, answer) satisfy search condition.
=======
        Args:
            `user_id` (int): Search shares by user_id

        Returns:
             List of shares  (questions, answer) satisfy search condition.
>>>>>>> dev
        """

        query = Share.query
        if not isinstance(args, dict):
            return send_error(message='Từ khoá truyền vào không đúng định dạng')
        user_id = None 
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if user_id is None :
            send_error(message='Không có từ khoá tìm kiếm.')

        is_filter = False
        if user_id is not None:
            query = query.filter(Share.user_id == user_id)
            is_filter = True

        if is_filter:
            shares = query.order_by(desc(Share.created_date)).all()
            if shares is not None and len(shares) > 0:
                results = list()
                for share in shares:
                    result = share.__dict__

                    # get user info
                    question = Question.query.filter_by(id=share.question_id).first()
                    result['question'] = question

                    # get user info
                    answer = Answer.query.filter_by(id=share.answer_id).first()
                    result['answer'] = answer

                    results.append(result)
                return send_result(data=marshal(results, ShareDto.model_response), message='Success')
            else:
                return send_result(message='Không tìm thấy kết quả chia sẻ')
        else:
            return send_error(message='Không tìm thấy kết quả. Vui lòng kiểm tra lại từ khoá tìm kiếm.')
