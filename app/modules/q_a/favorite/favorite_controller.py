#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask_restx import marshal
from sqlalchemy import and_

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.favorite.favorite import Favorite
from app.modules.q_a.favorite.favorite_dto import FavoriteDto
from app.modules.q_a.question.question import Question
from app.modules.user.user import User
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class FavoriteController(Controller):
    def search(self, args):
        """
        Search favorites.

        :param args: The dictionary-like parameters.

        :return:
        """
        if not isinstance(args, dict):
            return send_error(message='Could not parse params. Check again.')
        user_id, favorited_user_id, question_id, answer_id, comment_id, from_date, to_date = None, None, None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'favorited_user_id' in args:
            try:
                favorited_user_id = int(args['favorited_user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in args:
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in args:
            try:
                comment_id = int(args['comment_id'])
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
        if user_id is None and favorited_user_id is None and question_id is None and answer_id is None and comment_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide params to search.')
        query = db.session.query(Favorite)
        is_filter = False
        if user_id is not None:
            query = query.filter(Favorite.user_id == user_id)
            is_filter = True
        if favorited_user_id is not None:
            query = query.filter(Favorite.favorited_user_id == favorited_user_id)
            is_filter = True
        if question_id is not None:
            query = query.filter(Favorite.question_id == question_id)
            is_filter = True
        if answer_id is not None:
            query = query.filter(Favorite.answer_id == answer_id)
            is_filter = True
        if comment_id is not None:
            query = query.filter(Favorite.comment_id == comment_id)
            is_filter = True
        if from_date is not None:
            query = query.filter(Favorite.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Favorite.created_date <= to_date)
            is_filter = True
        if is_filter:
            favorites = query.all()
            if favorites is not None and len(favorites) > 0:
                return send_result(data=marshal(favorites, FavoriteDto.model_response), message='Success')
            else:
                return send_result(message='Could not find any favorites.')
        else:
            return send_error(message='Could not find favorites. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form. Please fill params.")
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        try:
            favorite = self._parse_favorite(data=data, favorite=None)
            db.session.add(favorite)
            db.session.commit()
            return send_result(message='Favorite was created successfully',
                               data=marshal(favorite, FavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create favorite.')

    # ----------region for user-------#
    def create_favorite_user(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included')
        if not 'favorited_user_id' in data:
            return send_error(message='The favorited_user_id must be included.')
        try:
            user_id = data['user_id']
            favorited_user_id = data['favorited_user_id']
            favorite = Favorite.query.filter(Favorite.user_id == user_id,
                                             Favorite.favorited_user_id == favorited_user_id).first()
            if favorite:
                return send_result(message='You are already favorited this user.')
            else:
                favorite = self._parse_favorite(data=data, favorite=None)
                favorite.created_date = datetime.utcnow()
                favorite.updated_date = datetime.utcnow()
                db.session.add(favorite)
                db.session.commit()
                # update user_favorite_count va user_favorited_count
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not add favorite user.')

    def delete_favorite_user(self, object_id):
        if object_id is None:
            return send_error(message='The ID must not be null')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if not favorite:
                return send_result(message='Could not find favorite with the ID {}'.format(object_id))
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='Delete successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete the favorite. Try again later.')

    # ----------region for question------#
    def create_favorite_question(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included')
        if not 'question_id' in data:
            return send_error(message='The question_id must be included.')
        try:
            user_id = data['user_id']
            question_id = data['question_id']
            favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.question_id == question_id).first()
            
            if favorite:
                return send_result(message='Bạn đã thích câu hỏi này.')
            else:
                favorite = self._parse_favorite(data=data, favorite=None)
                favorite.created_date = datetime.utcnow()
                favorite.updated_date = datetime.utcnow()
                db.session.add(favorite)
                db.session.commit()
                try:
                    # get user
                    user = User.query.filter_by(id=user_id).first()
                    # get user favorited
                    question = Question.query.filter_by(id=question_id).first()
                    user_favorited = User.query.filter_by(id=question.user_id).first()

                    # Update question_favorite_count cho bảng user
                    user.question_favorite_count += 1
                    # Update question_favorited_count cho bảng user
                    user_favorited.question_favorited_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create favorite. Try again.')

    def delete_favorite_question(self, object_id):
        if object_id is None:
            return send_error(message='The ID must not be null')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if not favorite:
                return send_result(message='Could not find favorite with the ID {}'.format(object_id))
            else:
                if favorite.question_id is None:
                    return send_result(message='You tried to hack our system. Stop doing this.')
                # xóa favorite từ bảng favorite
                db.session.delete(favorite)
                db.session.commit()
                try:
                    # Update question_favorite_count cho bảng user
                    user = User.query.filter_by(id=favorite.user_id).first()
                    user.question_favorite_count -= 1
                    # Update question_favorited_count cho bảng user
                    question = Question.query.filter_by(id=favorite.question_id).first()
                    user_favorited = User.query.filter_by(id=question.user_id).first()
                    user_favorited.question_favorited_count -= 1
                except Exception as e:
                    print(e.__str__())
                    pass
                return send_result(message='Delete successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete the favorite. Try again later.')

    # ---------region for answer---------#
    def create_favorite_answer(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included')
        if not 'answer_id' in data:
            return send_error(message='The answer_id must be included.')
        try:
            user_id = data['user_id']
            answer_id = data['answer_id']
            # check favorite
            favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.answer_id == answer_id).first()
            if favorite:
                return send_result(message='You favorited this answer')
            else:
                favorite = self._parse_favorite(data=data, favorite=None)
                favorite.created_date = datetime.utcnow()
                favorite.updated_date = datetime.utcnow()
                db.session.add(favorite)
                db.session.commit()
                # update other values
                try:
                    user = User.query.filter_by(id=user_id).first()
                    answer = Answer.query.filter_by(id=answer_id).first()
                    user_favorited = User.query.filter_by(id=answer.user_id).first()
                    # Update answer_favorite_count cho bảng user
                    user.answer_favorite_count += 1
                    # Update answer_favorited_count cho bảng user
                    user_favorited.answer_favorited_count += 1
                    db.session.commit()
                except Exception as e:
                    print(e.__str__())
                return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not created favorite. Try again.')

    def delete_favorite_answer(self, object_id):
        if object_id is None:
            return send_error(message='The ID must not be null')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if not favorite:
                return send_result(message='Could not find favorite with the ID {}'.format(object_id))
            else:
                if favorite.answer_id is None:
                    return send_result(message='You tried to hack our system. Stop doing this.')
                # xóa favorite từ bảng favorite
                db.session.delete(favorite)
                db.session.commit()
                try:
                    # Update question_favorite_count cho bảng user
                    user = User.query.filter_by(id=favorite.user_id).first()
                    user.answer_favorite_count -= 1
                    # Update question_favorited_count cho bảng user
                    answer = Answer.query.filter_by(id=favorite.answer_id).first()
                    user_favorited = User.query.filter_by(id=answer.user_id).first()
                    user_favorited.answer_favorited_count -= 1
                except Exception as e:
                    print(e.__str__())
                    pass
                return send_result(message='Delete successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete the favorite. Try again later.')

    # ---------region for comment--------#
    def create_favorite_comment(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included')
        if not 'comment_id' in data:
            return send_error(message='The comment_id must be included.')
        try:
            user_id = data['user_id']
            comment_id = data['comment_id']
            # check favorite
            favorite = Favorite.query.filter(Favorite.user_id == user_id, Favorite.answer_id == comment_id).first()
            if favorite:
                return send_result(message='You favorited this comment')
            else:
                favorite = self._parse_favorite(data=data, favorite=None)
                favorite.created_date = datetime.utcnow()
                favorite.updated_date = datetime.utcnow()
                db.session.add(favorite)
                db.session.commit()
                # # update other values
                # try:
                #     user = User.query.filter_by(id=user_id).first()
                #     comment = Comment.query.filter_by(id=comment_id).first()
                #     user_favorited = User.query.filter_by(id=comment.user_id).first()
                #     # Update comment_favorite_count cho bảng user
                #     user.commen
                #     # Update comment_favorited_count cho bảng user
                return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not created favorite. Try again.')

    def delete_favorite_comment(self, object_id):
        if object_id is None:
            return send_error(message='The ID must not be null')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if not favorite:
                return send_result(message='Could not find favorite with the ID {}'.format(object_id))
            else:
                if favorite.comment_id is None:
                    return send_result(message='You tried to hack out system. Stop doing this.')
                # xóa favorite từ bảng favorite
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='Delete successfully.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete the favorite. Try again later.')

    def get(self):
        try:
            favorites = Favorite.query.all()
            return send_result(data=marshal(favorites, FavoriteDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not load favorites.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Favorite ID is null.')
        favorite = Favorite.query.filter_by(id=object_id).first()
        if favorite is None:
            return send_error(message='Could not find favorite with ID {}'.format(object_id))
        else:
            return send_result(data=marshal(favorite, FavoriteDto.model_response), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='Favorite ID is null.')
        if data is None or not isinstance(data, dict):
            return send_error(message='Data is null or not in dictionary form. Check again.')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if favorite is None:
                return send_error(message='Favorite with the ID {} not found.'.format(object_id))
            else:
                favorite = self._parse_favorite(data=data, favorite=favorite)
                db.session.commit()
                return send_result(message='Update favorite successfully',
                                   data=marshal(favorite, FavoriteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update favorite.')

    def delete(self, object_id):
        if object_id is None:
            return send_error(message='ID must be included to delete.')
        try:
            favorite = Favorite.query.filter_by(id=object_id).first()
            if favorite is None:
                return send_error(message='Favorite with ID {} not found.'.format(object_id))
            else:
                db.session.delete(favorite)
                db.session.commit()
                return send_result(message='Favorite with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete favorite with ID {}.'.format(object_id))

    def _parse_favorite(self, data, favorite=None):
        if favorite is None:
            favorite = Favorite()
        if 'user_id' in data:
            try:
                favorite.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'favorited_user_id' in data:
            try:
                favorite.favorited_user_id = int(data['favorited_user_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'question_id' in data:
            try:
                favorite.question_id = int(data['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
            try:
                favorite.answer_id = int(data['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in data:
            try:
                favorite.comment_id = int(data['comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'favorite_date' in data:
        #     try:
        #         favorite.favorite_date = dateutil.parser.isoparse(data['favorite_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        return favorite
