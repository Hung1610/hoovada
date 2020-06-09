from datetime import datetime

import dateutil.parser
from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.favorite.favorite import Favorite
from app.modules.q_a.favorite.favorite_dto import FavoriteDto
from app.utils.response import send_error, send_result


class FavoriteController(Controller):
    def search(self, args):
        '''
        Search favorites.

        :param args: The dictionary-like parameters.

        :return:
        '''
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
            query = query.filter(Favorite.favorite_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Favorite.favorite_date <= to_date)
            is_filter = True
        if is_filter:
            favorites = query.all()
            if favorites is not None and len(favorites) > 0:
                return send_result(data=marshal(favorites, FavoriteDto.model), message='Success')
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
            return send_result(message='Favorite was created successfully', data=marshal(favorite, FavoriteDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create favorite.')

    def get(self):
        try:
            favorites = Favorite.query.all()
            return send_result(data=marshal(favorites, FavoriteDto.model), message='Success')
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
            return send_result(data=marshal(favorite, FavoriteDto.model), message='Success')

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
                return send_result(message='Update favorite successfully', data=marshal(favorite, FavoriteDto.model))
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
        if 'favorite_date' in data:
            try:
                favorite.favorite_date = dateutil.parser.isoparse(data['favorite_date'])
            except Exception as e:
                print(e.__str__())
                pass
        return favorite
