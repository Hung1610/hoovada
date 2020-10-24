#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import os
import json
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request, url_for
from flask import current_app as app
from flask_restx import marshal
from sqlalchemy import desc
from werkzeug.utils import secure_filename

# own modules
from app import db
from app.modules.auth.auth_controller import AuthController
from app.common.controller import Controller
from app.modules.q_a.answer.answer import Answer, FileTypeEnum
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.answer.favorite.favorite import AnswerFavorite
from app.modules.q_a.answer.voting.vote import AnswerVote, VotingStatusEnum
from app.modules.user.user import User
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error, send_result, paginated_result
from app.utils.sensitive_words import check_sensitive
from app.utils.file_handler import append_id, get_file_name_extension
from app.utils.util import encode_file_name
from app.utils.types import UserRole
from app.utils.wasabi import upload_file
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerController(Controller):
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count']

    def search(self, args):
        """
        Search answers.
        """
        
        if not isinstance(args, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
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

        # if user_id is None and question_id is None and from_date is None and to_date is None:
        #     send_error(message=messages.MSG_LACKING_QUERY_PARAMS)
        query = Answer.query.filter(Answer.is_deleted != True)
        is_filter = False
        if user_id is not None:
            query = query.filter(Answer.user_id == user_id)
            is_filter = True
        if question_id is not None:
            query = query.filter(Answer.question_id == question_id)
            is_filter = True
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
                    result = answer._asdict()
                    user = User.query.filter_by(id=answer.user_id).first()
                    result['user'] = user
                    # lay thong tin up_vote down_vote cho current user
                    current_user, _ = AuthController.get_logged_user(request)
                    if current_user:
                        vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                        if vote is not None:
                            result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                            result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                        favorite = AnswerFavorite.query.filter(AnswerFavorite.user_id == current_user.id,
                                                        AnswerFavorite.answer_id == answer.id).first()
                        result['is_favorited_by_me'] = True if favorite else False
                    results.append(result)
                return send_result(marshal(results, AnswerDto.model_response), message='Success')
            else:
                return send_result(message=messages.MSG_NOT_FOUND.format('Answer'))
        else:
             return send_error(message=messages.MSG_GET_FAILED)

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
        if not 'question_id' in data:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('question ID'))
        if not 'answer' in data:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('answer body'))

        current_user, _ = AuthController.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id
            answer = Answer.query.filter_by(question_id=data['question_id'], user_id=data['user_id']).first()
            if answer:
                if answer.is_deleted:
                    return send_error(message=messages.MSG_ISSUE.format('This has a hidden answer for this question. Consider recovering this.'), data={'answer_id': answer.id})
                return send_error(message=messages.MSG_ISSUE.format('This user already answered for this question'), data={'answer_id': answer.id})

        try:
            # add new answer
            answer = self._parse_answer(data=data, answer=None)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('answer content'))
            is_sensitive = check_sensitive(answer.answer)
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Content is not allowed'))
            answer.created_date = datetime.utcnow()
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.add(answer)
            db.session.commit()
            result = answer._asdict()
            # khi moi tao thi gia tri up_vote va down_vote cua nguoi dung hien gio la False
            result['up_vote'] = False
            result['down_vote'] = False
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Answer'), data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Answer', e))

    def create_with_file(self, object_id):
        if object_id is None:
            return send_error(messages.MSG_PLEASE_PROVIDE.format("Answer ID"))
        if 'file' not in request.files:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('file'))

        file_type = request.form.get('file_type', None)
        media_file = request.files.get('file', None)
        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('answer', object_id))
        question = answer.question

        if not media_file:
            return send_error(message=messages.MSG_NO_FILE)
        if not file_type:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('file type'))
        if FileTypeEnum(int(file_type)).name == FileTypeEnum.AUDIO.name and not question.allow_audio_answer:
            return send_error(message=messages.MSG_ISSUE.format('Question does not allow answer by audio.'))
        if FileTypeEnum(int(file_type)).name == FileTypeEnum.VIDEO.name and not question.allow_video_answer:
            return send_error(message=messages.MSG_ISSUE.format('Question does not allow answer by video.'))
        try:
            filename = media_file.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name(file_name) + ext
            bucket = 'hoovada'
            sub_folder = 'answer' + '/' + encode_file_name(str(answer.id))
            try:
                url = upload_file(file=media_file, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message=messages.MSG_ISSUE.format('Could not save your media file.'))

            answer.file_url = url
            answer.file_type = FileTypeEnum(int(file_type)).name
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.commit()
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            # update user information for answer
            result['user'] = user
            # khi moi tao thi gia tri up_vote va down_vote cua nguoi dung hien gio la False
            result['up_vote'] = False
            result['down_vote'] = False
            return send_result(message=messages.MSG_CREATE_SUCCESS.format('Answer media'), data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Answer media', e))

    def get(self, args):
        """
        Search answers.
        """
        try:
            if not isinstance(args, dict):
                return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
            user_id, question_id, from_date, to_date, is_deleted = None, None, None, None, None
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
            if args.get('is_deleted'):
                try:
                    is_deleted = bool(args['is_deleted'])
                except Exception as e:
                    print(e)
                    pass
            query = Answer.query
            query = query.join(User, isouter=True).filter(db.or_(Answer.user == None, User.is_deactivated != True))

            if not is_deleted:
                query = query.filter(Answer.is_deleted != True)
            else:
                query = query.filter(Answer.is_deleted == True)
            if user_id is not None:
                query = query.filter(Answer.user_id == user_id)
            if question_id is not None:
                query = query.filter(Answer.question_id == question_id)
            if from_date is not None:
                query = query.filter(Answer.created_date >= from_date)
            if to_date is not None:
                query = query.filter(Answer.created_date <= to_date)
                
            ordering_fields_desc = args.get('order_by_desc')
            if ordering_fields_desc:
                for ordering_field in ordering_fields_desc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Answer, ordering_field)
                        query = query.order_by(db.desc(column_to_sort))
            ordering_fields_asc = args.get('order_by_asc')
            if ordering_fields_asc:
                for ordering_field in ordering_fields_asc:
                    if ordering_field in self.allowed_ordering_fields:
                        column_to_sort = getattr(Answer, ordering_field)
                        query = query.order_by(db.asc(column_to_sort))
                        
            page, per_page = args.get('page', 1), args.get('per_page', 10)
            query = query.paginate(page, per_page, error_out=True)
            res, code = paginated_result(query)

            # get user information for each answer.
            results = []
            for answer in res.get('data'):
                result = answer._asdict()
                user = User.query.filter_by(id=answer.user_id).first()
                result['user'] = user
                # lay thong tin up_vote down_vote cho current user
                current_user, _ = AuthController.get_logged_user(request)
                if current_user:
                    vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = AnswerFavorite.query.filter(AnswerFavorite.user_id == current_user.id,
                                                    AnswerFavorite.answer_id == answer.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                results.append(result)
            res['data'] = marshal(results, AnswerDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_GET_FAILED.format('Answer'))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(messages.MSG_PLEASE_PROVIDE.format("Answer ID"))
        answer = Answer.query.filter_by(id=object_id).first()
        if answer is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Answer', object_id))
        else:
            # get user information for each answer.
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            # lay thong tin up_vote down_vote cho current user
            current_user, _ = AuthController.get_logged_user(request)
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = AnswerFavorite.query.filter(AnswerFavorite.user_id == current_user.id,
                                                AnswerFavorite.answer_id == answer.id).first()
                result['is_favorited_by_me'] = True if favorite else False
            # return send_result(marshal(result, AnswerDto.model_response), message='Success')
            return send_result(data=marshal(result, AnswerDto.model_response))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format("Answer ID"))
        if data is None or not isinstance(data, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
        # if not 'question_id' in data:
        #     return send_error(message="Please fill the question ID")
        # if not 'answer' in data:
        #     return send_error(message='Please fill the answer body before sending.')
        # if not 'user_id' in data:
        #     return send_error(message='Please fill the user ID')
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Answer', object_id))

            current_user, _ = AuthController.get_logged_user(request)
            # Check is admin or has permission
            if answer.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
                return send_error(code=401, message=messages.MSG_NOT_DO_ACTION)

            answer = self._parse_answer(data=data, answer=answer)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('answer content'))
            is_sensitive = check_sensitive(answer.answer)
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Comment content not allowed'))
            if answer.question_id is None:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('question_id'))
            if answer.user_id is None:
                return send_error(message=messages.MSG_PLEASE_PROVIDE.format('user_id'))
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.commit()
            # get user information for each answer.
            result = answer._asdict()
            user = User.query.filter_by(id=answer.user_id).first()
            result['user'] = user
            # lay thong tin up_vote down_vote cho current user
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = AnswerFavorite.query.filter(AnswerFavorite.user_id == current_user.id,
                                                AnswerFavorite.answer_id == answer.id).first()
                result['is_favorited_by_me'] = True if favorite else False
            # return send_result(marshal(result, AnswerDto.model_response), message='Success')
            return send_result(message=messages.MSG_UPDATE_SUCCESS.format('Answer'), data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_UPDATE_FAILED.format('Answer', e))

    def delete(self, object_id):
        try:
            answer = Answer.query.filter_by(id=object_id).first()
            if answer is None:
                return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Answer', object_id))
            else:
                db.session.delete(answer)
                db.session.commit()
                return send_result(message=messages.MSG_DELETE_SUCCESS)
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_DELETE_SUCCESS)

    def _parse_answer(self, data, answer=None):
        if answer is None:
            answer = Answer()
        # if 'created_date' in data:
        #     try:
        #         answer.created_date = dateutil.parser.isoparse(data['created_date'])
        #         # answer.created_date = dateutil.parser.isoparse(data['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'updated_date' in data:
        #     try:
        #         answer.updated_date = dateutil.parser.isoparse(data['updated_date']) #dateutil.parser.isoparse(data['update_date'])
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
        return answer
