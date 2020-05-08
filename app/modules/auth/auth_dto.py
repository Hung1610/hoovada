from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AuthDto(Dto):
    name = 'auth'
    api = Namespace(name)
    model = api.model(name, {
        'email': fields.String(required=True),
        'password_hash': fields.String(required=True)
    })
