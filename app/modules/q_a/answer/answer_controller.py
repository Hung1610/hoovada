#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from bs4 import BeautifulSoup
from flask import current_app, g, request
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.answer.bookmark.bookmark_controller import AnswerBookmarkController
from common.controllers.controller import Controller
from common.utils.onesignal_notif import push_basic_notification
from common.enum import FileTypeEnum, VotingStatusEnum
from common.utils.file_handler import get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import check_sensitive
from common.utils.types import UserRole
from common.utils.util import encode_file_name
from common.utils.wasabi import upload_file

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Answer = db.get_model('Answer')
AnswerVote = db.get_model('AnswerVote')
UserFriend = db.get_model('UserFriend')
UserFollow = db.get_model('UserFollow')


class AnswerController(Controller):
    query_classname = 'Answer'
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        if not 'question_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('question ID'))
        if not 'answer' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer body'))

        current_user, _ = current_app.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id
            answer = Answer.query.with_deleted().filter_by(question_id=data['question_id'], user_id=data['user_id']).first()
            if answer:
                if answer.is_deleted:
                    return send_error(message=messages.ERR_ISSUE.format('This user already answered the question but it is hidden!'), data={'answer_id': answer.id})
                return send_error(message=messages.ERR_ISSUE.format('This user already answered for this question!'), data={'answer_id': answer.id})

        try:
            answer = self._parse_answer(data=data, answer=None)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer content'))
            
            text = ' '.join(BeautifulSoup(answer.answer, "html.parser").stripped_strings)
            if len(text.split()) < 100:
                return send_error(message=messages.ERR_CONTENT_TOO_SHORT.format('100'))

            is_sensitive = check_sensitive(text)
            if is_sensitive:
                return send_error(message=messages.ERR_BODY_INAPPROPRIATE)

            answer.created_date = datetime.utcnow()
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.add(answer)
            db.session.commit()


            # TODO: if this is invited question then update status in invited_question table



            # Add bookmark for the creator
            controller = AnswerBookmarkController()
            controller.create(answer_id=answer.id)
            result = answer._asdict()
            result['up_vote'] = False
            result['down_vote'] = False
            
            #if answer.user:
            #    followers = UserFollow.query.with_entities(UserFollow.follower_id)\
            #        .filter(UserFollow.followed_id == answer.user.id).all()
            #    follower_ids = [follower[0] for follower in followers]
            #    new_answer_notify_user_list.send(answer.id, follower_ids)
            #    g.friend_belong_to_user_id = answer.user.id
            #    friends = UserFriend.query\
            #        .filter(\
            #            (UserFriend.friended_id == answer.user.id) | \
            #            (UserFriend.friend_id == answer.user.id))\
            #        .all()
            #    friend_ids = [friend.adaptive_friend_id for friend in friends]
            #    new_answer_notify_user_list.send(answer.id, friend_ids)

            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Answer'), data=marshal(result, AnswerDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Answer', str(e)))

    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Answer ID"))
        if 'file' not in request.files:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))

        file_type = request.form.get('file_type', None)
        media_file = request.files.get('file', None)
        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('answer', object_id))
        question = answer.question

        if not media_file:
            return send_error(message=messages.ERR_NO_FILE)
        if not file_type:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file type'))
        if FileTypeEnum(int(file_type)).name == FileTypeEnum.AUDIO.name and not question.allow_audio_answer:
            return send_error(message=messages.ERR_ISSUE.format('Question does not allow answer by audio.'))
        if FileTypeEnum(int(file_type)).name == FileTypeEnum.VIDEO.name and not question.allow_video_answer:
            return send_error(message=messages.ERR_ISSUE.format('Question does not allow answer by video.'))
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            sub_folder = 'answer' + '/' + encode_file_name(str(answer.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.ERR_ISSUE.format('Could not save your media file.'))

            answer.file_url = url
            answer.file_type = FileTypeEnum(int(file_type)).name
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.commit()
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            result['up_vote'] = False
            result['down_vote'] = False
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Answer media'), data=marshal(result, AnswerDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format('Answer media', e))


    def get_query(self):
        query = self.get_model_class().query
        query = query.join(User, isouter=True).filter(db.or_(Answer.user == None, User.is_deactivated != True))
        return query


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('user_id'):
            get_my_own = False
            if g.current_user:
                if params.get('user_id') == str(g.current_user.id):
                    get_my_own = True
            if not get_my_own:
                query = query.filter(db.func.coalesce(Answer.is_anonymous, False) != True)
        if params.get('from_date'):
            query = query.filter(Answer.created_date >= dateutil.parser.isoparse(params.get('from_date')))
        if params.get('to_date'):
            query = query.filter(Answer.created_date <= dateutil.parser.isoparse(params.get('to_date')))

        return query


    def get(self, args):

        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            current_user = g.current_user
            # get user information for each answer.
            results = []
            for answer in res.get('data'):
                result = answer._asdict()
                user = User.query.filter_by(id=answer.user_id).first()
                result['user'] = user
                if current_user:
                    vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False

                results.append(result)
            res['data'] = marshal(results, AnswerDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format('Answer', e))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Answer ID"))
        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Answer', object_id))
        else:
            # get user information for each answer.
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            current_user, _ = current_app.get_logged_user(request)
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            return send_result(data=marshal(result, AnswerDto.model_response))


    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format("Answer ID"))

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        # if not 'question_id' in data:
        #     return send_error(message="Please fill the question ID")
        # if not 'answer' in data:
        #     return send_error(message='Please fill the answer body before sending.')
        # if not 'user_id' in data:
        #     return send_error(message='Please fill the user ID')
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Answer', object_id))

            current_user, _ = current_app.get_logged_user(request)
            if current_user is None or (answer.user_id != current_user.id and not UserRole.is_admin(current_user.admin)):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            answer = self._parse_answer(data=data, answer=answer)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer content'))
            is_sensitive = check_sensitive(' '.join(BeautifulSoup(answer.answer, "html.parser").stripped_strings))
            if is_sensitive:
                return send_error(message=messages.ERR_ISSUE.format('Comment content not allowed'))
            if answer.question_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('question_id'))
            if answer.user_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_id'))

            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.commit()

            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False

            # return send_result(marshal(result, AnswerDto.model_response), message='Success')
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Answer'), data=marshal(result, AnswerDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format('Answer', e))


    def delete(self, object_id):
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('Answer', object_id))
            
            current_user, _ = current_app.get_logged_user(request)
            if current_user is None or (answer.user_id != current_user.id and not UserRole.is_admin(current_user.admin)):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(answer)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format('Answer', e))


    def _parse_answer(self, data, answer=None):
        if answer is None:
            answer = Answer()
        if 'accepted' in data:
            try:
                answer.accepted = bool(data['accepted'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer' in data:
            answer.answer = data['answer']
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
            
        if 'is_deleted' in data:
            try:
                answer.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                print(e)
                pass
        if 'allow_comments' in data:
            try:
                answer.allow_comments = bool(data['allow_comments'])
            except Exception as e:
                answer.allow_comments = True
                print(e.__str__())
                pass
        if 'allow_improvement' in data:
            try:
                answer.allow_improvement = bool(data['allow_improvement'])
            except Exception as e:
                answer.allow_improvement = True
                print(e.__str__())
                pass
        if 'is_anonymous' in data:
            try:
                answer.is_anonymous = bool(data['is_anonymous'])
            except Exception as e:
                answer.is_anonymous = False
                print(e.__str__())
                pass
        return answer
