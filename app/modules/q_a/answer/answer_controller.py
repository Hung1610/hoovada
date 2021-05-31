#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g, request
from flask_restx import marshal

# own modules
from common.db import db
from app.constants import messages
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.answer.bookmark.bookmark_controller import AnswerBookmarkController
from common.controllers.controller import Controller
from common.enum import FileTypeEnum, VotingStatusEnum
from common.utils.file_handler import get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
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
AnswerBookmark = db.get_model('AnswerBookmark')
UserFriend = db.get_model('UserFriend')
UserFollow = db.get_model('UserFollow')
Question = db.get_model('Question')
QuestionUserInvite = db.get_model('QuestionUserInvite')
QuestionBookmark = db.get_model('QuestionBookmark')
QuestionVote = db.get_model('QuestionVote')
UserAnswerProfile = db.get_model('UserAnswerProfile')
UserLanguage = db.get_model('UserLanguage')
UserEmployment = db.get_model('UserEmployment')
UserLocation = db.get_model('UserLocation')
UserEducation = db.get_model('UserEducation')
UserTopic = db.get_model('UserTopic')


class AnswerController(Controller):
    query_classname = 'Answer'
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count']
    

    def create(self, data):
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'question_id' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('question ID'))
        
        if not 'answer' in data or data['answer'] == "":
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer body'))

        current_user = g.current_user
        user_profile, error_res, field_count = self._validate_user_profile(current_user, data)
        if error_res:
            return error_res
        
        if field_count > 1:
            return send_error(message=messages.ERR_USER_INFO_MORE_THAN_1)
        
        data['user_id'] = current_user.id
        answer = Answer.query.with_deleted().filter_by(question_id=data['question_id'], user_id=data['user_id']).first()
        if answer:            
            return send_error(message=messages.ERR_USER_ALREADY_ANSWERED, data={'answer_id': answer.id})

        answer = self._parse_answer(data=data, answer=None)
        try:

            answer.created_date = datetime.utcnow()
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.add(answer)
            if user_profile:
                if user_profile[1] == 'UserLanguage':
                    answer.user_language_id = user_profile[0].id
                if user_profile[1] == 'UserEmployment':
                    answer.user_employment_id = user_profile[0].id
                if user_profile[1] == 'UserEducation':
                    answer.user_education_id = user_profile[0].id
                if user_profile[1] == 'UserLocation':
                    answer.user_location_id = user_profile[0].id
                if user_profile[1] == 'UserTopic':
                    answer.user_topic_id = user_profile[0].id

            question_user_invite = QuestionUserInvite.query.filter_by(user_id=data['user_id'], question_id=data['question_id']).first()
            if question_user_invite:
                question_user_invite.status = 1
            else:
                new_question_user_invite = QuestionUserInvite()
                new_question_user_invite.user_id = data['user_id']
                new_question_user_invite.question_id = data['question_id']
                new_question_user_invite.status = 1
                db.session.add(new_question_user_invite)
            
            # Add bookmark for the creator
            bookmark_controller = AnswerBookmarkController()
            bookmark_controller.create(answer_id=answer.id)
            db.session.commit()

            result = answer._asdict()
            result['is_upvoted_by_me'] = False
            result['is_downvoted_by_me'] = False
            result['is_bookmarked_by_me'] = True

            # if answer.user:
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

            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, AnswerDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("Answer ID"))

        if 'file' not in request.files:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('file'))

        file_type = request.form.get('file_type', None)
        media_file = request.files.get('file', None)

        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND)
        
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

            # Add bookmark for the creator
            bookmark_controller = AnswerBookmarkController()
            bookmark_controller.create(answer_id=answer.id)
            db.session.commit()
            
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            result['is_upvoted_by_me'] = False
            result['is_downvoted_by_me'] = False
            result['is_bookmarked_by_me'] = True

            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(result, AnswerDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


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
                        result['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == current_user.id, AnswerBookmark.answer_id == answer.id).first()
                    if bookmark is not None:
                        result['is_bookmarked_by_me'] = True if bookmark else False


                    question_id = result['question'].id
                    vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question_id).first()
                    if vote is not None:
                        result['question']['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['question']['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id, QuestionBookmark.question_id == question_id).first()
                    if bookmark is not None:
                        result['question']['is_bookmarked_by_me'] = True if bookmark else False

                results.append(result)
            res['data'] = marshal(results, AnswerDto.model_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("id"))

        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        try:
            # get user information for each answer.
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user

            current_user = g.current_user
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == current_user.id, AnswerBookmark.answer_id == answer.id).first()
                if bookmark is not None:
                    result['is_bookmarked_by_me'] = True if bookmark else False


                question_id = result['question'].id
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question_id).first()
                if vote is not None:
                    result['question']['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['question']['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id, QuestionBookmark.question_id == question_id).first()
                if bookmark is not None:
                    result['question']['is_bookmarked_by_me'] = True if bookmark else False

            return send_result(data=marshal(result, AnswerDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format("id"))

        if data is None or not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        current_user = g.current_user
        user_profile, error_res, field_count = self._validate_user_profile(current_user, data)
        if error_res:
            return error_res

        if field_count > 1:
            return send_error(message=messages.ERR_USER_INFO_MORE_THAN_1)
        
        if answer.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        if 'answer' in data:
            if data['answer'] == '':
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('answer content'))

        answer = self._parse_answer(data=data, answer=answer)
        try:

            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            if user_profile:
                if user_profile[1] == 'UserLanguage':
                    answer.user_language_id = user_profile[0].id
                    answer.user_employment_id = None
                    answer.user_education_id = None
                    answer.user_location_id = None
                    answer.user_topic_id = None
                if user_profile[1] == 'UserEmployment':
                    answer.user_employment_id = user_profile[0].id
                    answer.user_language_id = None
                    answer.user_education_id = None
                    answer.user_location_id = None
                    answer.user_topic_id = None
                if user_profile[1] == 'UserEducation':
                    answer.user_education_id = user_profile[0].id
                    answer.user_language_id = None
                    answer.user_employment_id = None
                    answer.user_location_id = None
                    answer.user_topic_id = None
                if user_profile[1] == 'UserLocation':
                    answer.user_location_id = user_profile[0].id
                    answer.user_education_id = None
                    answer.user_language_id = None
                    answer.user_employment_id = None
                    answer.user_topic_id = None
                if user_profile[1] == 'UserTopic':
                    answer.user_topic_id = user_profile[0].id
                    answer.user_education_id = None
                    answer.user_language_id = None
                    answer.user_employment_id = None
                    answer.user_location_id = None
            db.session.commit()

            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user

            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == current_user.id, AnswerBookmark.answer_id == answer.id).first()
                if bookmark is not None:
                    result['is_bookmarked_by_me'] = True if bookmark else False

                question_id = result['question'].id
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question_id).first()
                if vote is not None:
                    result['question']['is_upvoted_by_me'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['question']['is_downvoted_by_me'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id, QuestionBookmark.question_id == question_id).first()
                if bookmark is not None:
                    result['question']['is_bookmarked_by_me'] = True if bookmark else False

            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(result, AnswerDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if answer.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(answer)
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def get_query(self):
        query = self.get_model_class().query
        query = query.join(User, isouter=True).filter(db.or_(Answer.user == None, User.is_deactivated == False))
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
            try:
                answer.answer = data['answer']
            except Exception as e:
                print(e.__str__())
                pass

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
                
        if 'allow_comments' in data:
            try:
                answer.allow_comments = bool(data['allow_comments'])
            except Exception as e:
                answer.allow_comments = True
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    answer.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    answer.allow_voting = True
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


    def _validate_user_profile(self, current_user, data):
        user_profile = None
        user_profile_data_count = 0
        error = None
        if 'user_language_id' in data:
            user_language = UserLanguage.query.filter_by(id=data['user_language_id']).first()
            if not user_language:
                return None, send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('UserLanguage', data['user_language_id'])), user_profile_data_count
            if user_language.user_id != current_user.id:
                return None, send_error(code=401, message=messages.ERR_NOT_AUTHORIZED), user_profile_data_count
            user_profile_data_count += 1
            user_profile = user_language, 'UserLanguage'
        
        if 'user_employment_id' in data:
            user_employment = UserEmployment.query.filter_by(id=data['user_employment_id']).first()
            if not user_employment:
                return None, send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('UserEmployment', data['user_employment_id'])), user_profile_data_count
            if user_employment.user_id != current_user.id:
                return None, send_error(code=401, message=messages.ERR_NOT_AUTHORIZED), user_profile_data_count
            user_profile_data_count += 1
            user_profile = user_employment, 'UserEmployment'
        
        if 'user_location_id' in data:
            user_location = UserLocation.query.filter_by(id=data['user_location_id']).first()
            if not user_location:
                return None, send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('UserLocation', data['user_location_id'])), user_profile_data_count
            if user_location.user_id != current_user.id:
                return None, send_error(code=401, message=messages.ERR_NOT_AUTHORIZED), user_profile_data_count
            user_profile_data_count += 1
            user_profile = user_location, 'UserLocation'
        
        if 'user_education_id' in data:
            user_education = UserEducation.query.filter_by(id=data['user_education_id']).first()
            if not user_education:
                return None, send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('UserEducation', data['user_education_id'])), user_profile_data_count
            if user_education.user_id != current_user.id:
                return None, send_error(code=401, message=messages.ERR_NOT_AUTHORIZED), user_profile_data_count
            user_profile_data_count += 1
            user_profile = user_education, 'UserEducation'
        
        if 'user_topic_id' in data:
            user_topic = UserTopic.query.filter_by(id=data['user_topic_id']).first()
            if not user_topic:
                return None, send_error(message=messages.ERR_NOT_FOUND_WITH_ID.format('UserTopic', data['user_topic_id'])), user_profile_data_count
            if user_topic.user_id != current_user.id:
                return None, send_error(code=401, message=messages.ERR_NOT_AUTHORIZED), user_profile_data_count
            user_profile_data_count += 1
            user_profile = user_topic, 'UserTopic'
        return user_profile, None, user_profile_data_count