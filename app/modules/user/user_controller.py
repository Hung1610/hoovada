#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
import os
from datetime import datetime
import dateutil.parser

# third-party modules
from flask import url_for, request, send_file
from flask_restx import marshal

# own modules
from app import db
from app.modules.auth.auth_controller import AuthController
from app.modules.user.user import User
from app.modules.user.user_dto import UserDto
from app.utils.response import send_result, send_error
from app.modules.common.controller import Controller
from app.settings.config import BaseConfig as Config
from app.utils.util import encode_file_name

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


AVATAR_FOLDER = Config.AVATAR_FOLDER
IMAGE_FOLDER = Config.IMAGE_FOLDER


class UserController(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary type")
        if not 'email' in data and not 'password' in data:
            return send_error(message="Please fill email and password")
        try:
            exist_user = User.query.filter_by(email=data['email']).first()
            if not exist_user:
                user = self._parse_user(data, None)
                db.session.add(user)
                db.session.commit()
                return send_result(message='User was created successfully', data=marshal(user, UserDto.model_response))
            else:
                return send_error(message='User exists')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create user. Check again')

    def get(self):
        try:
            users = User.query.all()
            return send_result(data=marshal(users, UserDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load error, please try again later.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message="The user ID must not be null.")
        try:
            user = User.query.filter_by(id=object_id).first()
            if user is None:
                return send_error(data="Could not find user by this id")
            else:
                # when call to this function, increase the profile_views
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


    def update(self, object_id, data):
        '''
        Doest now allow to update `id`, `email`, `password`, `profile_views`.

        :param object_id:

        :param data:

        :return:
        '''
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
        user, message = AuthController.get_logged_user(request)
        # user = User.query.filter_by(id=id).first()
        if user is None:
            return send_error(message)

        photo = args['avatar']
        if photo:
            file_name = 'user_' + str(user.id) + '_avatar'
            file_name = encode_file_name(file_name) + ".png"
            try:
                if not os.path.exists(IMAGE_FOLDER):
                    os.mkdir(IMAGE_FOLDER)
                if not os.path.exists(AVATAR_FOLDER):
                    os.mkdir(AVATAR_FOLDER)
                photo.save(os.path.join(AVATAR_FOLDER, file_name))
                user.profile_pic_url = url_for('user_avatar', filename=file_name)
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload avatar successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your avatar.')
        else:
            return send_error(message='Please attach or check your photo before uploading.')


    def get_avatar(self):
        # upload here
        filename = request.args.get('filename')
        filename = os.path.join(AVATAR_FOLDER, filename)
        if os.path.exists(filename):
            return send_file(filename)
        else:
            return send_error(message='Avatar does not exist. Upload it first.')
        # user, message = AuthController.get_logged_user(request)
        # # user = User.query.filter_by(id=id).first()
        # if user is None:
        #     return send_error(message)
        # return user.avatar


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
        if 'email_confirmed_at' in data:
            try:
                user.email_confirmed_at = datetime.fromisoformat(data['email_confirmed_at'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'profile_pic_url' in data:
            user.profile_pic_url = data['profile_pic_url']
        if 'profile_pic_data_url' in data:
            user.profile_pic_data_url = data['profile_pic_data_url']
        if 'admin' in data:
            try:
                user.admin = bool(data['admin'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'active' in data:
            try:
                user.active = bool(data['active'])
            except Exception as e:
                print(e.__str__())
                pass

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
        if 'city' in data:
            user.city = data['city']
        if 'country' in data:
            user.country = data['country']
        if 'website_url' in data:
            user.website_url = data['website_url']

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
        if 'job_role' in data:
            user.job_role = data['job_role']
        if 'company' in data:
            user.company = data['company']

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
                user.last_message_read_time = datetime.fromisoformat(data['last_message_read_time'])
            except Exception as e:
                print(e.__str__())
                pass
        return user
