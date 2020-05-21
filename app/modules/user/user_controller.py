from flask_restx import marshal

from app import db
from app.modules.user.user import User
from app.modules.user.user_dto import UserDto
from app.utils.response import send_result, send_error
from app.modules.common.controller import Controller


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
                return send_result(message='User was created successfully', data=marshal(user, UserDto.model))
            else:
                return send_error(message='User exists')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create user. Check again')

    def get(self):
        try:
            users = User.query.all()
            return send_result(data=marshal(users, UserDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load error, please try again later.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message="The user ID must not be null.")
        user = User.query.filter_by(user_id=object_id).first()
        if user is None:
            return send_error(data="Could not find user by this id")
        else:
            return send_result(data=marshal(user, UserDto.model))

    def update(self, object_id, data):
        try:
            user = User.query.filter_by(user_id=object_id).first()
            if not user:
                return send_error(message='User not found')
            else:
                user = self._parse_user(data=data, user=user)
                db.session.commit()
                return send_result(message='Update successfully', data=marshal(user, UserDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update user')

    def delete(self, object_id):
        try:
            user = User.query.filter_by(user_id=object_id).first()
            if not user:
                return send_error(message='User not found')
            else:
                db.session.delete(user)
                db.session.commit()
                return send_result(message='User was deleted successfully')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete user')

    def _parse_user(self, data, user=None):
        pass
        # name, surname, middlename, fullname, age, birthday, home_address, home_country, home_city, home_street, home_geo_long, home_geo_lat, phone, email, username, passwordHash, blocked, token, facebook, instagram, vkontakte, avatar, isadmin = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        # if 'name' in data:
        #     name = data['name']
        # if 'surname' in data:
        #     surname = data['surname']
        # if 'middlename' in data:
        #     middlename = data['middlename']
        # if 'fullname' in data:
        #     fullname = data['fullname']
        # if 'age' in data:
        #     age = int(data['age'])
        # if 'birthday' in data:
        #     try:
        #         birthday = date.fromisoformat(data['birthday'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        #
        # if 'home_address' in data:
        #     home_address = data['home_address']
        # if 'home_country' in data:
        #     home_country = data['home_country']
        # if 'home_city' in data:
        #     home_city = data['home_city']
        # if 'home_street' in data:
        #     home_street = data['home_street']
        # if 'home_geo_long' in data:
        #     home_geo_long = data['home_geo_long']
        # if 'home_geo_lat' in data:
        #     home_geo_lat = data['home_geo_lat']
        #
        # if 'phone' in data:
        #     phone = data['phone']
        # # email bat buoc phai co
        # email = data['email']
        # if 'username' in data:
        #     username = data['username']
        # # password bat buoc phai co
        # password = data['password']
        # passwordHash = flask_bcrypt.generate_password_hash(password)
        # if 'blocked' in data:
        #     blocked = bool(data['blocked'])
        #
        # if 'token' in data:
        #     token = data['token']
        # if 'facebook' in data:
        #     facebook = data['facebook']
        # if 'instagram' in data:
        #     instagram = data['instagram']
        # if 'vkontakte' in data:
        #     vkontakte = data['vkontakte']
        # if 'avatar' in data:
        #     avatar = data['avatar']
        # if 'isadmin' in data:
        #     isadmin = bool(data['isadmin'])
        #
        # if user is None:
        #     user = User(name=name, surname=surname, middlename=middlename, fullname=fullname, age=age,
        #                 birthday=birthday, home_address=home_address, home_country=home_country, home_city=home_city,
        #                 home_street=home_street, home_geo_long=home_geo_long, home_geo_lat=home_geo_lat, phone=phone,
        #                 email=email, username=username,
        #                 password_hash=passwordHash, blocked=blocked, token=token,
        #                 facebook=facebook, instagram=instagram, vkontakte=vkontakte, avatar=avatar, isadmin=isadmin)
        # else:
        #     user.name = name
        #     user.surname = surname
        #     user.middlename = middlename
        #     user.fullname = fullname
        #     user.age = age
        #     user.birthday = birthday
        #
        #     user.home_address = home_address
        #     user.home_country = home_country
        #     user.home_city = home_city
        #     user.home_street = home_street
        #     user.home_geo_long = home_geo_long
        #     user.home_geo_lat = home_geo_lat
        #
        #     user.phone = phone
        #     user.email = email
        #     user.username = username
        #     user.password_hash = passwordHash
        #     user.blocked = blocked
        #
        #     user.token = token
        #     user.facebook = facebook
        #     user.instagram = instagram
        #     user.vkontakte = vkontakte
        #     user.avatar = avatar
        #     user.isadmin = isadmin
        # return user
