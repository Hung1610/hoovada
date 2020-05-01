from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AuthDto(Dto):
    name = 'auth'
    api = Namespace(name)
    model = api.model('auth_details', {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })
