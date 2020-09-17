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
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer, FileTypeEnum
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.q_a.answer.favorite.favorite import AnswerFavorite
from app.modules.q_a.question.question import Question
from app.modules.q_a.answer.voting.vote import AnswerVote
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.comment.comment_dto import CommentDto
from app.modules.user.user import User
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive
from app.utils.file_handler import append_id, get_file_name_extension
from app.utils.util import encode_file_name
from app.utils.wasabi import upload_file
from app.constants import messages

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerController(Controller):

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
        # if 'created_date' in args:
        #     try:
        #         created_date = dateutil.parser.isoparse(args['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'updated_date' in args:
        #     try:
        #         updated_date = dateutil.parser.isoparse(args['updated_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
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

        if user_id is None and question_id is None and from_date is None and to_date is None:
            send_error(message=messages.MSG_LACKING_QUERY_PARAMS)
        query = Answer.query.filter(Answer.is_deleted != True)
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
                    result = answer._asdict()
                    user = User.query.filter_by(id=answer.user_id).first()
                    result['user'] = user
                    # lay thong tin up_vote down_vote cho current user
                    current_user, _ = AuthController.get_logged_user(request)
                    if current_user:
                        vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                        if vote is not None:
                            result['up_vote'] = vote.up_vote
                            result['down_vote'] = vote.down_vote
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

        try:
            answer = Answer.query.filter_by(question_id=data['question_id'], user_id=data['user_id']).first()
            if answer:
                return send_error(message=messages.MSG_ISSUE.format('This user already answered for this question'))
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
        question = Question.query.filter_by(id=answer.question_id).first()
        if question is None:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('answer', answer.question_id))

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
                url = upload_file(file=media_file, file_name=file_name, bucket=bucket, sub_folder=sub_folder)
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

    def create_comment(self, object_id, data):
        if object_id is None:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format("Answer ID"))
        if not isinstance(data, dict):
            return send_error(message=messages.MSG_WRONG_DATA_FORMAT)
        answer = Answer.query.filter_by(id=object_id).first()
        if not answer:
            return send_error(message=messages.MSG_NOT_FOUND_WITH_ID.format('Answer', object_id))
        if not 'comment' in data:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format("comment body"))
        if not 'answer_id' in data:
            return send_error(message=messages.MSG_PLEASE_PROVIDE.format('answer_id'))
        answer = Answer.query.filter(id == data['answer_id']).first()
        if not answer:
            return send_error(message=messages.MSG_NOT_FOUND.format('answer'))
        if not answer.allow_comments:
            return send_error(message=messages.MSG_ISSUE.format('answer'))
            
        data['answer_id'] = answer.id
        current_user, _ = AuthController.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id

        try:

            comment = self._parse_comment(data=data, comment=None)
            is_sensitive = check_sensitive(comment.comment)
            if is_sensitive:
                return send_error(message=messages.MSG_ISSUE.format('Comment content not allowed'))
            comment.created_date = datetime.utcnow()
            comment.updated_date = datetime.utcnow()
            db.session.add(comment)
            db.session.commit()
            # update comment count for user
            try:
                user = User.query.filter_by(id=comment.user_id).first()
                user.comment_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                pass

            # update comment count cho answer.
            try:
                answer = Answer.query.filter_by(id=comment.answer_id).first()
                answer.comment_count += 1
                db.session.commit()
            except Exception as e:
                print(e.__str__())
                pass
            try:
                result = comment.__dict__
                # get thong tin user
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(message=messages.MSG_CREATE_SUCCESS.format('Comment'),
                                   data=marshal(result, CommentDto.model_response))
            except Exception as e:
                print(e.__str__())
                return send_result(data=marshal(comment, CommentDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.MSG_CREATE_FAILED.format('Comment', e))

    def get(self):
        """
        [DEPRECATED]
        Hàm này được giữ lại, tuy nhiên sẽ không publish API, answers chỉ được nhận về qua search.
        :return:
        """
        try:
            answers = Answer.query.order_by(desc(Answer.created_date)).limit(50).all()
            return send_result(data=marshal(answers, AnswerDto.model_response), message='Success')
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
                    result['up_vote'] = vote.up_vote
                    result['down_vote'] = vote.down_vote
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
            current_user, _ = AuthController.get_logged_user(request)
            if current_user:
                vote = AnswerVote.query.filter(AnswerVote.user_id == current_user.id, AnswerVote.answer_id == answer.id).first()
                if vote is not None:
                    result['up_vote'] = vote.up_vote
                    result['down_vote'] = vote.down_vote
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
                # ------- delete from other tables---------#
                # delete from vote

                # delete from comment

                # delete from report

                # delete from share

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
        if 'user_hidden' in data:
            try:
                answer.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                answer.user_hidden = False
                print(e.__str__())
                pass
        return answer


    def _parse_comment(self, data, comment=None):
        if comment is None:
            comment = Comment()
        if 'comment' in data:
            comment.comment = data['comment']
        if 'answer_id' in data:
            try:
                comment.answer_id = int(data['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'user_id' in data:
            try:
                comment.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        return comment