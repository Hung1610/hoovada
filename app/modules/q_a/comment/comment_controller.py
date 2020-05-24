from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.comment.comment_dto import CommentDto
from app.utils.response import send_error, send_result


class CommentController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'answer_id' in data:
            return send_error(message="The answer_id must be inclued")
        if not 'user_id' in data:
            return send_error(message="The user_id must be included")
        try:
            comment = self._parse_comment(data=data, comment=None)
            db.session.add(comment)
            db.session.commit()
            return send_result(message='Comment was created successfully', data=marshal(comment, CommentDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create comment')

    def get(self):
        try:
            comments = Comment.query.all()
            return send_result(data=marshal(comments, CommentDto.model), message='Success')
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
            return send_result(data=marshal(comment, CommentDto.model), message='Success')

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
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(comment, CommentDto.model))
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
        if 'comment_body' in data:
            comment.comment_body = data['comment_body']
        if 'created_date' in data:
            try:
                comment.created_date = datetime.fromisoformat(data['created_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in data:
            try:
                comment.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
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
