from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class UserDto(Dto):
    name = 'user'
    api = Namespace(name)
    model = api.model(name, {
        'user_id': fields.Integer(required=False),
        'name':fields.String(required=False)
        # some other fields will be done later
    })
