#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
import os
from datetime import datetime

import dateutil.parser
# third-party modules
from flask import current_app, request, send_file, url_for, g
from flask_restx import marshal
from sqlalchemy import desc, func, text

# own modules
from app.app import db
from app.modules.user.user_dto import UserDto
from common.controllers.controller import Controller
from common.utils.file_handler import get_file_name_extension
from common.utils.response import paginated_result, send_error, send_result
from common.utils.types import UserRole
from common.utils.util import encode_file_name
from common.utils.wasabi import delete_file, upload_file

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
Reputation = db.get_model('Reputation')
Topic = db.get_model('Topic')


class UserController(Controller):
    query_classname = 'User'
    special_filtering_fields = ['from_date', 'to_date', 'endorsed_topic_id', 'is_endorsed', 'email_or_name']
    allowed_ordering_fields = ['question_count', 'answer_count', 'post_count']

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        if not 'email' in data and not 'password' in data:
            return send_error(message="Please fill email and password")
        try:
            exist_user = User.query.filter_by(email=data['email']).first()
            if not exist_user:
                user = self._parse_user(data, None)
                user.display_name = user.display_name or data['email']
                user.password_hash = user.password_hash or data['email']
                user.admin = UserRole.ADMIN
                db.session.add(user)
                db.session.commit()
                return send_result(message='User was created successfully', data=marshal(user, UserDto.model_response))
            else:
                return send_error(message='User exists')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create user. Check again')

    def get_query(self):
        query = super().get_query()
        query = query.filter(User.is_deactivated != True)
        return query    

    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('email_or_name'):
            query = query.filter((User.display_name == params.get('email_or_name')) | (User.email == params.get('email_or_name')))
        if params.get('is_endorsed') and g.endorsed_topic_id:
            topic = Topic.query.get(g.endorsed_topic_id)
            user_ids = [user.id for user in topic.endorsed_users]
            query = query.filter(User.id.in_(user_ids))

        return query

    def get(self, args):
        try:
            g.endorsed_topic_id = args.get('endorsed_topic_id')
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            res['data'] = marshal(res['data'], UserDto.model_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load error, please try again later.")
    
    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count}, message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load topics. Contact your administrator for solution.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message="The user ID must not be null.")
        try:
            current_user, _ = current_app.get_logged_user(request)
            user = User.query.filter_by(id=object_id).first()
            if user is None:
                return send_error(data="Could not find user by this id")
            if user.is_private:
                return send_error(data="This user info is private")
            # when call to this function, increase the profile_views
            if current_user.id != user.id:
                user.profile_views += 1
                db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get user by ID {}.'.format(object_id))


    def get_by_user_name(self, user_name):
        if user_name is None:
            return send_error(message="The user_name must not be null.")
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if user is None:
                return send_error(data="Could not find user by this user name")
            else:
                # when call to this function, increase the profile_views
                user.profile_views += 1
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get user by ID {}.'.format(user_name))

    def update(self, user_name, data):
        """
        Doest now allow to update `id`, `email`, `password`, `profile_views`.

        :param user_name:

        :param data:

        :return:
        """
        if not isinstance(data, dict):
            return send_error(message='You must pass dictionary-like data.')
        if 'id' in data:
            return send_error(message='Could not update ID.')
        if 'email' in data:
            return send_error(message='Email update is not allowed here.')
        if 'password' in data and data['password'] is None:
            return send_error(message='Password update is now allowed here.')
        if 'profile_views' in data:
            return send_error(message='Profile views is not allowed to update.')
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if not user:
                return send_error(message='User not found')
            else:
                user = self._parse_user(data=data, user=user)
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(user, UserDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update user')


    def delete(self, user_name):
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if not user:
                return send_error(message='User not found')
            else:
                db.session.delete(user)
                db.session.commit()
                return send_result(message='User was deleted successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user')


    def upload_avatar(self, args):
        if not isinstance(args, dict) or not 'avatar' in args:
            return send_error(message='Your request does not contain avatar.')
        # upload here
        user, _ = current_app.get_logged_user(request)
        # user = User.query.filter_by(id=id).first()
        if user is None:
            return send_error('You are not logged in')

        photo = args['avatar']
        if photo:
            filename = photo.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name('user_' + str(user.id) + '_avatar') + ext
            bucket = 'hoovada'
            sub_folder = 'user' + '/' + encode_file_name(str(user.id))
            try:
                if user.profile_pic_url:
                    delete_file(file_path=user.profile_pic_url)
                url = upload_file(file=photo, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your media file.')

            try:
                user.profile_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload avatar successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your avatar.')
        else:
            return send_error(message='Please attach or check your photo before uploading.')


    def upload_cover(self, args):
        if not isinstance(args, dict) or not 'cover' in args:
            return send_error(message='Your request does not contain avatar.')
        # upload here
        user, _ = current_app.get_logged_user(request)
        # user = User.query.filter_by(id=id).first()
        if user is None:
            return send_error('You are not logged in')

        photo = args['cover']
        if photo:
            filename = photo.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name('user_' + str(user.id) + '_cover') + ext
            bucket = 'hoovada'
            sub_folder = 'user' + '/' + encode_file_name(str(user.id))
            try:
                if user.cover_pic_url:
                    delete_file(file_path=user.cover_pic_url)
                url = upload_file(file=photo, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your media file.')

            try:
                user.cover_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload avatar successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your avatar.')
        else:
            return send_error(message='Please attach or check your photo before uploading.')


    def get_avatar(self):
        # upload here
        # filename = request.args.get('filename')
        # filename = os.path.join(AVATAR_FOLDER, filename)
        # if os.path.exists(filename):
        #     return send_file(filename)
        # else:
        #     return send_error(message='Avatar does not exist. Upload it first.')
        user, _ = current_app.get_logged_user(request)
        # user = User.query.filter_by(id=id).first()
        if user is None:
            return send_error('You are not logged in')
        return user.profile_pic_url


    def _parse_user(self, data, user=None):
        if user is None:
            user = User()
        if 'display_name' in data:
            user.display_name = data['display_name']
        if 'title' in data:
            user.title = data['title']

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'middle_name' in data:
            user.middle_name = data['middle_name']
        if 'last_name' in data:
            user.last_name = data['last_name']

        if 'gender' in data:
            user.gender = data['gender']
        if 'age' in data:
            user.age = data['age']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(password=data['password'])

        if 'last_seen' in data:
            try:
                user.last_seen = dateutil.parser.isoparse(data['last_seen'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'joined_date' in data:
            try:
                user.joined_date = dateutil.parser.isoparse(data['joined_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'confirmed' in data:
            try:
                user.confirmed = bool(data['confirmed'])
            except Exception as e:
                print(e.__str__())
                pass
        else:
            user.confirmed = 1
        if 'email_confirmed_at' in data:
            try:
                user.email_confirmed_at = dateutil.parser.isoparse(data['email_confirmed_at'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'profile_pic_url' in data:
            user.profile_pic_url = data['profile_pic_url']
        if 'admin' in data:
            try:
                user.admin = UserRole.ADMIN if bool(data['admin']) is True else None
            except Exception as e:
                print(e.__str__())
                pass
        if 'active' in data:
            try:
                user.active = bool(data['active'])
            except Exception as e:
                print(e.__str__())
                pass
        else:
            user.active = 1

        if 'reputation' in data:
            try:
                user.reputation = int(data['reputation'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'profile_views' in data:  # doan nay can sua de chi co the view duoc, ma ko set duoc
            pass
            # try:
            #     user.profile_views = int(data['profile_views'])
            # except Exception as e:
            #     print(e.__str__())
            #     pass

        if 'about_me' in data:
            user.about_me = data['about_me']
        if 'about_me_markdown' in data:
            user.about_me_markdown = data['about_me_markdown']
        if 'about_me_html' in data:
            user.about_me_html = data['about_me_html']

        if 'people_reached' in data:
            try:
                user.people_reached = int(data['people_reached'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'show_email_publicly_setting' in data:
            try:
                user.show_email_publicly_setting = bool(data['show_email_publicly_setting'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'hoovada_digests_setting' in data:
            try:
                user.hoovada_digests_setting = bool(data['hoovada_digests_setting'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'hoovada_digests_frequency_setting' in data:
            user.hoovada_digests_frequency_setting = data['hoovada_digests_frequency_setting']

        if 'questions_you_asked_or_followed_setting' in data:
            try:
                user.questions_you_asked_or_followed_setting = bool(data['questions_you_asked_or_followed_setting'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'questions_you_asked_or_followed_frequency_setting' in data:
            user.questions_you_asked_or_followed_frequency_setting = data[
                'questions_you_asked_or_followed_frequency_setting']

        if 'people_you_follow_setting' in data:
            try:
                user.people_you_follow_setting = bool(data['people_you_follow_setting'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'people_you_follow_frequency_setting' in data:
            user.people_you_follow_frequency_setting = data['people_you_follow_frequency_setting']

        if 'email_stories_topics_setting' in data:
            try:
                user.email_stories_topics_setting = bool(data['email_stories_topics_setting'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'email_stories_topics_frequency_setting' in data:
            user.email_stories_topics_frequency_setting = data['email_stories_topics_frequency_setting']
        if 'last_message_read_time' in data:
            try:
                user.last_message_read_time = dateutil.parser.isoparse(data['last_message_read_time'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'is_private' in data:
            try:
                user.is_private = bool(data['is_private'])
            except Exception as e:
                user.is_private = False
                print(e.__str__())
                pass
        if 'is_deactivated' in data:
            try:
                user.is_deactivated = bool(data['is_deactivated'])
            except Exception as e:
                user.is_deactivated = False
                print(e.__str__())
                pass
        if 'show_nsfw' in data:
            try:
                user.show_nsfw = bool(data['show_nsfw'])
            except Exception as e:
                user.show_nsfw = True
                print(e.__str__())
                pass
        return user

    def get_user_hot(self,args):
        page = 1
        page_size = 20

        if args.get('page') and args['page'] > 0:
            try:
                page = args['page']
            except Exception as e:
                print(e.__str__())
                pass

        if args.get('per_page') and args['per_page'] > 0 :
            try:
                page_size = args['per_page']
            except Exception as e:
                print(e.__str__())
                pass

        if page > 0 :
            page = page - 1

        query = db.session.query(User).outerjoin(Reputation).group_by(User).order_by(desc(func.sum(Reputation.score)))
        users = query.offset(page * page_size).limit(page_size).all()

        if users is not None and len(users) > 0:
            return send_result(data=marshal(users, UserDto.model_response), message='Success')
        else:
            return send_result(message='Could not find any users')
