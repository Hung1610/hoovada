#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
from datetime import datetime
from http import HTTPStatus

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal
from sqlalchemy import desc, func

# own modules
from app.constants import messages
from common.db import db
from app.modules.user.user_dto import UserDto
from common.controllers.controller import Controller
from common.utils.file_handler import get_file_name_extension
from common.utils.onesignal_notif import push_notif_to_specific_users
from common.utils.response import paginated_result, send_error, send_result
from common.utils.types import UserRole
from common.utils.util import encode_file_name
from common.utils.wasabi import delete_file, upload_file
from common.utils.sensitive_words import is_sensitive
from common.es import get_model
from common.utils.util import strip_tags

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


User = db.get_model('User')
UserFriend = db.get_model('UserFriend')
SocialAccount = db.get_model('SocialAccount')
Reputation = db.get_model('Reputation')
Topic = db.get_model('Topic')
ESUser = get_model('User')
ESUserFriend = get_model('UserFriend')


class UserController(Controller):
    query_classname = 'User'
    special_filtering_fields = ['from_date', 'to_date', 'endorsed_topic_id', 'is_endorsed', 'email_or_name', 'is_mutual_friend']
    allowed_ordering_fields = ['question_count', 'answer_count', 'post_count', 'reputation']


    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'email' in data and not 'password' in data:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('email and password'))
        
        try:
            exist_user = User.query.filter_by(email=data['email']).first()
            if exist_user is not None:
                return send_error(message=messages.ERR_EMAIL_ALREADY_EXIST)

            user = self._parse_user(data, None)

            if is_sensitive(user.about_me) or is_sensitive(user.display_name):
                return send_error(message=messages.ERR_USER_INAPPROPRIATE)

            user.display_name = user.display_name or data['email']
            user.password_hash = user.password_hash or data['email']
            user.admin = UserRole.ADMIN
            db.session.add(user)
            db.session.flush()
            user_dsl = ESUser(_id=user.id, display_name=user.display_name, email=user.email,
                            gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
            user_dsl.save()
            db.session.commit()

            return send_result(message=messages.MSG_CREATE_SUCCESS, data=marshal(user, UserDto.model_response))

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):
        try:
            g.endorsed_topic_id = args.get('endorsed_topic_id')
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            res['data'] = marshal(res['data'], UserDto.model_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))
    

    def get_count(self, args):
        try:
            count = self.get_query_results_count(args)
            return send_result({'count': count}, message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        
        if object_id is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("id"))
        
        try:
            current_user = g.current_user
            user = User.query.filter_by(id=object_id).first()
            if user is None:
                return send_error(message=messages.ERR_NOT_LOGIN)
            
            if user.is_private is True or user.is_deactivated is True:
                return send_error(data=messages.ERR_USER_PRIVATE_OR_DEACTIVATED)

            # when call to this function, increase the profile_views
            if current_user.id != user.id:
                user.profile_views += 1
                db.session.commit()

            return send_result(data=marshal(user, UserDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_user_name(self, user_name):
        if user_name is None:
            return send_error(messages.ERR_PLEASE_PROVIDE.format("user name"))
        
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if user is None:
                return send_error(message=messages.ERR_NOT_LOGIN)

            if user.is_private or user.is_deactivated is True:
                return send_error(data=messages.ERR_USER_PRIVATE_OR_DEACTIVATED)

            # when call to this function, increase the profile_views
            user.profile_views += 1
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_social_account(self, user_name, args):
        
        if user_name is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user_name'))
        
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if user is None:
                return send_error(message=messages.ERR_NOT_LOGIN)

            social_accounts_query = SocialAccount.query.filter(SocialAccount.user_id == user.id)
            if args.get('provider'):
                social_accounts_query.filter(SocialAccount.provider == args.get('provider'))
            
            return send_result(data=marshal(social_accounts_query, UserDto.model_social_response), message=messages.MSG_GET_SUCCESS)

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def update(self, user_name, data):
        """ Does not allow to update `id`, `email`, `password`, `profile_views` """

        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
       
        if 'id' in data:
            return send_error(message=messages.ERR_NOT_AUTHORIZED)

        if 'email' in data:
            return send_error(message=messages.ERR_NOT_AUTHORIZED)

        if 'password' in data and data['password'] is None:
            return send_error(message=messages.ERR_NOT_AUTHORIZED)

        if 'profile_views' in data:
            return send_error(message=messages.ERR_NOT_AUTHORIZED)

        if 'gender' in data:
            try:
                data['gender'] = str(data['gender'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'about_me' in data:
            try:
                data['about_me'] = data['about_me'].strip()
            except Exception as e:
                print(e.__str__())
                pass

        if 'display_name' in data:
            try:
                data['display_name'] = data['display_name'].strip()
                if data['display_name'] == '':
                    return send_error(message=messages.ERR_PLEASE_PROVIDE.format('display_name'))                
            except Exception as e:
                print(e.__str__())
                pass

        if 'first_name' in data:
            try:
                data['first_name'] = data['first_name'].strip()
                if data['first_name'] == '':
                    return send_error(message=messages.ERR_PLEASE_PROVIDE.format('first_name'))                
            except Exception as e:
                print(e.__str__())
                pass

        if 'last_name' in data:
            try:
                data['last_name'] = data['last_name'].strip()
                if data['last_name'] == '':
                    return send_error(message=messages.ERR_PLEASE_PROVIDE.format('last_name'))                
            except Exception as e:
                print(e.__str__())
                pass

        try:
            user = User.query.filter_by(display_name=user_name).first()
            if not user:
                return send_error(message=messages.ERR_NOT_LOGIN)

            user = self._parse_user(data=data, user=user)

            if is_sensitive(user.about_me) or is_sensitive(user.display_name) or is_sensitive(user.first_name) or is_sensitive(user.last_name):
                return send_error(message=messages.ERR_USER_INAPPROPRIATE)

            if user.show_fullname_instead_of_display_name is True and user.last_name is not None and user.first_name is not None:
                full_name = user.last_name.strip() + " " + user.first_name.strip()
                if len(full_name) > 0:
                    user.display_name = full_name

            user_dsl = ESUser(_id=user.id)
            user_dsl.update(display_name=user.display_name, email=user.email,
                gender=user.gender, age=user.age, reputation=user.reputation, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
            # update display_name and profile_pic_url to search
            try:
                user_friends = UserFriend.query.filter(\
                    (UserFriend.friended_id == user.id) |\
                    (UserFriend.friend_id == user.id) \
                ).all()
                for user_friend in user_friends:
                    user_friend_dsl = ESUserFriend(_id=user_friend.id)
                    user_friend_dsl_doc = user_friend_dsl.get(id=user_friend.id)
                    if user_friend_dsl_doc and user_friend_dsl_doc.friend_id == user.id:
                        user_friend_dsl.update(friend_display_name=user.display_name, friend_profile_pic_url=user.profile_pic_url)
                    if user_friend_dsl_doc and user_friend_dsl_doc.friend_id == user.id:
                        user_friend_dsl.update(friended_display_name=user.display_name, friended_profile_pic_url=user.profile_pic_url)
            except Exception as e:
                print(e.__str__())
                pass

            db.session.commit()
            return send_result(message=messages.MSG_UPDATE_SUCCESS, data=marshal(user, UserDto.model_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, user_name):
        try:
            user = User.query.filter_by(display_name=user_name).first()
            if not user:
                return send_error(message=messages.ERR_NOT_LOGIN)
            
            db.session.delete(user)
            user_dsl = ESUser(_id=user.id)
            user_dsl.delete()
            db.session.commit()
            return send_result(message=messages.MSG_DELETE_SUCCESS)

        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def upload_avatar(self, args):

        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if  'avatar' not in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('avatar'))

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
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))

            try:
                user.profile_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload avatar successfully.')
            except Exception as e:
                db.session.rollback()
                print(e.__str__())
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))

        else:
            user.profile_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted avatar successfully.')


    def upload_document(self, args):

        if not isinstance(args, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

        if 'doc' not in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('document'))
   
        user = g.current_user
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
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))

            try:
                user.document_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload doc successfully.')
            except Exception as e:
                db.session.rollback()
                print(e.__str__())
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))
        
        else:
            user.document_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted doc successfully.')


    def upload_cover(self, args):

        if not isinstance(args, dict):
            return send_error(message='Your request does not contain avatar.')

        if  'cover' not in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('user cover photo'))


        user = g.current_user
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
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))

            try:
                user.cover_pic_url = url
                db.session.commit()
                return send_result(data=marshal(user, UserDto.model_response), message='Upload cover successfully.')
            except Exception as e:
                db.session.rollback()
                print(e.__str__())
                return send_error(message=messages.ERR_FAILED_UPLOAD.format(str(e)))
        else:
            user.cover_pic_url = None
            db.session.commit()
            return send_result(data=marshal(user, UserDto.model_response), message='Deleted cover successfully.')


    def get_avatar(self):
        user = g.current_user
        return user.profile_pic_url


    def _parse_user(self, data, user=None):
        if user is None:
            user = User()
        user._from_dict(data)
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


    def notify_user_mention(self, args):

        if 'user_mentioned_id' not in args:
            return send_error(message=messages.ERR_LACKING_GET_PARAMS.format('User mentioned id'))

        user_mention_id = g.current_user.id
        user_mentioned_ids = args.get('user_mentioned_id')
        
        try:
            for user_mentioned_id in user_mentioned_ids:
                if user_mention_id == user_mentioned_id:
                    return send_error(message='You can not mention yourself')

                user_mention_info = User.query.filter_by(id=user_mention_id).first()
                if not user_mention_info:
                    return send_error(message=messages.ERR_NOT_FOUND)
                
                push_notif_to_specific_users(message="{} has mention you to {}'s comment".format(user_mention_info.display_name, 
                                                                                                user_mention_info.display_name),
                                                                                                user_ids=[user_mentioned_id])
                return send_result(message='Success')

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_query(self):
        query = super().get_query()
        query = query.filter(User.is_deactivated != True)
        return query    


    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        if params.get('email_or_name'):
            query = query.filter(\
                (User.display_name.like('%' + params.get('email_or_name') + '%')) | \
                (User.email.like('%' + params.get('email_or_name') + '%')))
        
        if params.get('is_endorsed') and g.endorsed_topic_id:
            topic = Topic.query.get(g.endorsed_topic_id)
            user_ids = [user.id for user in topic.endorsed_users]
            query = query.filter(User.id.in_(user_ids))

        if params.get('is_mutual_friend') and g.current_user:
            g.friend_belong_to_user_id = g.current_user.id
            my_friends_query = UserFriend.query.filter(db.or_(UserFriend.friended_id == g.current_user.id, UserFriend.friend_id == g.current_user.id))\
                    .filter(UserFriend.is_approved == True)
            
            friend_ids = [friend.adaptive_friend_id for friend in my_friends_query]
            g.mutual_friend_ids = friend_ids
            mutual_friends_query = UserFriend.query.filter(db.or_(UserFriend.friended_id.in_(friend_ids), UserFriend.friend_id.in_(friend_ids)))\
                .filter((UserFriend.friended_id != g.current_user.id) & (UserFriend.friend_id != g.current_user.id))
            
            mutual_friend_ids = [friend.adaptive_friend_id for friend in mutual_friends_query]
            mutual_friend_ids = [friend_id for friend_id in mutual_friend_ids if friend_id not in friend_ids]
            query = query.filter(User.id.in_(mutual_friend_ids))   

        return query
