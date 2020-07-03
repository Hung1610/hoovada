from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.comment.comment_dto import CommentDto
from app.modules.q_a.question.question import Question
from app.modules.user.user import User
from app.utils.response import send_error, send_result


class CommentController(Controller):

    def search(self, args):
        '''
        Search comments by params.

        :param args: Arguments in dictionary form.

        :return:
        '''
        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        # user_id, question_id, answer_id = None, None, None
        user_id, answer_id = None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'question_id' in args:
        #     try:
        #         question_id = int(args['question_id'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'answer_id' in args:
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if user_id is None and answer_id is None:
            send_error(message='Provide params to search.')
        query = db.session.query(Comment)
        is_filter = False
        if user_id is not None:
            query = query.filter(Comment.user_id == user_id)
            is_filter = True
        # if question_id is not None:
        #     query = query.filter(Comment.question_id == question_id)
        #     is_filter = True
        if answer_id is not None:
            query = query.filter(Comment.answer_id == answer_id)
            is_filter = True
        if is_filter:
            comments = query.all()
            if comments is not None and len(comments) > 0:
                results = list()
                for comment in comments:
                    result = comment.__dict__
                    # get thong tin user
                    user = User.query.filter_by(id=comment.user_id).first()
                    result['user'] = user
                    results.append(result)
                return send_result(marshal(results, CommentDto.model_response), message='Success')
            else:
                return send_result(message='Could not find any comments.')
        else:
            return send_error(message='Could not find comments. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'comment' in data:
            return send_error(message="The comment body must be included")
        if not 'user_id' in data:
            return send_error(message="The user_id must be included")
        if not 'answer_id' in data:
            return send_error(message='The answer_id must be included.')
        try:
            comment = self._parse_comment(data=data, comment=None)
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
                return send_result(message='Comment was created successfully',
                                   data=marshal(result, CommentDto.model_response))
            except Exception as e:
                print(e.__str__())
                return send_result(data=marshal(comment, CommentDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create comment')

    def get(self):
        '''
        Giữ lại hàm này, tuy nhiên sẽ không cho phép nhận lại toàn bộ comments, mà nhận theo question hoặc answer thông qua hàm search.
        :return:
        '''
        try:
            comments = Comment.query.all()
            return send_result(data=marshal(comments, CommentDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not load comments. Contact your administrator for solution.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error('Comment ID is null')
        comment = Comment.query.filter_by(id=object_id).first()
        if comment is None:
            return send_error(message='Could not find comment with the ID {}'.format(object_id))
        else:
            try:
                result = comment.__dict__
                # get thong tin user
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(data=marshal(result, CommentDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not get comment with the ID {}'.format(object_id))

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='Comment ID is null')
        if data is None or not isinstance(data, dict):
            return send_error('Data is null or not in dictionary form. Check again.')
        try:
            comment = Comment.query.filter_by(id=object_id).first()
            if comment is None:
                return send_error(message='Comment with the ID {} not found.'.format(object_id))
            else:
                comment = self._parse_comment(data=data, comment=comment)
                comment.updated_date = datetime.utcnow()
                db.session.commit()
                result = comment.__dict__
                # get thong tin user
                user = User.query.filter_by(id=comment.user_id).first()
                result['user'] = user
                return send_result(message='Update successfully', data=marshal(result, CommentDto.model_response))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update comment.')

    def delete(self, object_id):
        try:
            comment = Comment.query.filter_by(id=object_id)
            if comment is None:
                return send_error(message='Comment with the ID {} not found.'.format(object_id))
            else:
                # ---------Delete from other tables----------#
                # delete from vote

                # delete from share

                # delete favorite

                db.session.delete(comment)
                db.session.commit()
                return send_result(message='Comment with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete comment with the ID {}.'.format(object_id))

    def _parse_comment(self, data, comment=None):
        if comment is None:
            comment = Comment()
        if 'comment' in data:
            comment.comment = data['comment']
        # if 'created_date' in data:
        #     try:
        #         comment.created_date = datetime.fromisoformat(data['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'question_id' in data:
        #     try:
        #         comment.question_id = int(data['question_id'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
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
