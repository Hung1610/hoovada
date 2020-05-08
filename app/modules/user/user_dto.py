from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class UserDto(Dto):
    name = 'user'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(required=False),
        'display_name':fields.String(required=False),
        'title':fields.String(required=False),

        'first_name': fields.String(required=False),
        'middle_name':fields.String(required=False),
        'last_name': fields.String(required=False),

        'gender': fields.String(required=False),
        'age': fields.String(required=False),
        'email': fields.String(required=False),
        'password_hash': fields.String(required=False)

        # '': fields.String(required=False),
        # '': fields.String(required=False),
        # '': fields.String(required=False),
        # '': fields.String(required=False),
        #
        # '': fields.String(required=False),
        # '': fields.String(required=False),
        # '': fields.String(required=False),
        # '': fields.String(required=False),


    })
