from app.modules.common.view import Resource
from app.modules.user.user_dto import UserDto
from .user_controller import UserController
from ..auth.decorator import admin_token_required, token_required

api = UserDto.api
_user = UserDto.model


@api.route('')
class UserList(Resource):
    @admin_token_required
    @api.marshal_list_with(_user)
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
    @token_required
    @api.marshal_with(_user)
    def get(self, user_id):
        pass

    @api.expect(_user, validate=True)
    def put(self, user_id):
        pass

    @token_required
    def delete(self, user_id):
        pass
