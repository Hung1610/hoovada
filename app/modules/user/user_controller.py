#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
import os
from datetime import datetime
import dateutil.parser

# third-party modules
from flask import current_app, request, g
from flask_restx import marshal
from sqlalchemy import desc, func

# own modules
from common.db import db
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
SocialAccount = db.get_model('SocialAccount')
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


    def get_social_account(self, user_name, args):
        if user_name is None:
            return send_error(message="The user_name must not be null.")
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if user is None:
                return send_error(data="Could not find user by this user name")
            social_accounts_query = SocialAccount.query.filter(SocialAccount.user_id == user.id)
            if args.get('provider'):
                social_accounts_query.filter(SocialAccount.provider == args.get('provider'))
            
            return send_result(data=marshal(social_accounts_query, UserDto.model_social_response))
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
            user.profile_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted avatar successfully.')


    def upload_document(self, args):
        if not isinstance(args, dict) or not 'doc' in args:
            return send_error(message='Your request does not contain doc.')
        # upload here
        user, _ = current_app.get_logged_user(request)
        if user is None:
            return send_error('You are not logged in')

        photo = args['doc']
        if photo:
            filename = photo.filename
            file_name, ext = get_file_name_extension(filename)
            file_name = encode_file_name('user_' + str(user.id) + '_doc') + ext
            sub_folder = 'user' + '/' + encode_file_name(str(user.id))
            try:
                if user.document_pic_url:
                    delete_file(file_path=user.document_pic_url)
                url = upload_file(file=photo, file_name=file_name, sub_folder=sub_folder)
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your media file.')

            try:
                user.document_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload doc successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your doc.')
        else:
            user.document_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted doc successfully.')


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
                return send_result(data=marshal(user, UserDto.model_response), message='Upload cover successfully.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not save your avatar.')
        else:
            user.cover_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted cover successfully.')


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
        if data.get('display_name'):
            user.display_name = data['display_name']
        if data.get('title'):
            user.title = data['title']
        if data.get('first_name'):
            user.first_name = data['first_name']
        if data.get('middle_name'):
            user.middle_name = data['middle_name']
        if data.get('last_name'):
            user.last_name = data['last_name']
        if data.get('birthday'):
            user.birthday = dateutil.parser.isoparse(data['birthday'])
        if data.get('gender'):
            user.gender = data['gender']
        if data.get('age'):
            user.age = data['age']
        if data.get('email'):
            user.email = data['email']
        if data.get('password'):
            user.set_password(password=data['password'])
        if data.get('last_seen'):
            try:
                user.last_seen = dateutil.parser.isoparse(data['last_seen'])
            except Exception as e:
                print(e.__str__())
                pass
        if data.get('joined_date'):
            try:
                user.joined_date = dateutil.parser.isoparse(data['joined_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if data.get('confirmed'):
            try:
                user.confirmed = bool(data['confirmed'])
            except Exception as e:
                print(e.__str__())
                pass
        else:
            user.confirmed = 1
        if data.get('email_confirmed_at'):
            try:
                user.email_confirmed_at = dateutil.parser.isoparse(data['email_confirmed_at'])
            except Exception as e:
                print(e.__str__())
                pass
        if data.get('profile_pic_url'):
            user.profile_pic_url = data['profile_pic_url']
        if data.get('admin'):
            try:
                user.admin = UserRole.ADMIN if bool(data['admin']) is True else None
            except Exception as e:
                print(e.__str__())
                pass
        if data.get('active'):
            try:
                user.active = bool(data['active'])
            except Exception as e:
                print(e.__str__())
                pass
        else:
            user.active = 1
        if data.get('about_me'):
            user.about_me = data['about_me']
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

        if 'new_answer_notify_settings' in data:
            user.new_answer_notify_settings = data.get('new_answer_notify_settings')

        if 'new_answer_email_settings' in data:
            user.new_answer_email_settings = data.get('new_answer_email_settings')

        if 'my_question_notify_settings' in data:
            user.my_question_notify_settings = data.get('my_question_notify_settings')

        if 'my_question_email_settings' in data:
            user.my_question_email_settings = data.get('my_question_email_settings')

        if 'new_question_comment_notify_settings' in data:
            user.new_question_comment_notify_settings = data.get('new_question_comment_notify_settings')

        if 'new_question_comment_email_settings' in data:
            user.new_question_comment_email_settings = data.get('new_question_comment_email_settings')

        if 'new_answer_comment_notify_settings' in data:
            user.new_answer_comment_notify_settings = data.get('new_answer_comment_notify_settings')

        if 'new_answer_comment_email_settings' in data:
            user.new_answer_comment_email_settings = data.get('new_answer_comment_email_settings')

        if 'new_article_comment_notify_settings' in data:
            user.new_article_comment_notify_settings = data.get('new_article_comment_notify_settings')

        if 'new_article_comment_email_settings' in data:
            user.new_article_comment_email_settings = data.get('new_article_comment_email_settings')

        if 'question_invite_notify_settings' in data:
            user.question_invite_notify_settings = data.get('question_invite_notify_settings')

        if 'question_invite_email_settings' in data:
            user.question_invite_email_settings = data.get('question_invite_email_settings')

        if 'friend_request_notify_settings' in data:
            user.friend_request_notify_settings = data.get('friend_request_notify_settings')

        if 'friend_request_email_settings' in data:
            user.friend_request_email_settings = data.get('friend_request_email_settings')

        if 'follow_notify_settings' in data:
            user.follow_notify_settings = data.get('follow_notify_settings')

        if 'follow_email_settings' in data:
            user.follow_email_settings = data.get('follow_email_settings')

        if 'followed_new_publication_notify_settings' in data:
            user.followed_new_publication_notify_settings = data.get('followed_new_publication_notify_settings')

        if 'followed_new_publication_email_settings' in data:
            user.followed_new_publication_email_settings = data.get('followed_new_publication_email_settings')

        if 'admin_interaction_notify_settings' in data:
            user.admin_interaction_notify_settings = data.get('admin_interaction_notify_settings')

        if 'admin_interaction_email_settings' in data:
            user.admin_interaction_email_settings = data.get('admin_interaction_email_settings')

        if 'last_message_read_time' in data:
            try:
                user.last_message_read_time = dateutil.parser.isoparse(data['last_message_read_time'])
            except Exception as e:
                print(e.__str__())
                pass
        if data.get('is_private'):
            try:
                user.is_private = bool(data['is_private'])
            except Exception as e:
                user.is_private = False
                print(e.__str__())
                pass
        if data.get('is_deactivated'):
            try:
                user.is_deactivated = bool(data['is_deactivated'])
            except Exception as e:
                user.is_deactivated = False
                print(e.__str__())
                pass
        if data.get('verified_document'):
            try:
                user.verified_document = bool(data['verified_document'])
            except Exception as e:
                user.verified_document = False
                print(e.__str__())
                pass
        if data.get('show_nsfw'):
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
