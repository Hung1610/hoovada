from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto
from .user_controller import UserController

api = UserDto.api
_user = UserDto.model


@api.route('')
class UserList(Resource):
    def get(self):
        """
        Returns all users in the system.
        """
        controller = UserController()
        return controller.get()

    @api.expect(_user)
    def post(self):
        pass


@api.route('/<int:user_id>')
class User(Resource):
    def get(self, user_id):
        pass

    def post(self, user_id):
        pass

    def delete(self, user_id):
        pass
