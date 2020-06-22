from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AuthDto(Dto):
    name = 'auth'
    api = Namespace(name)
    model_register = api.model('register', {
        'display_name': fields.String(required=False),
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })

    model_login = api.model('login', {
        'email': fields.String(required=True),
        'password': fields.String(requried=True)
    })

    message_response = api.model('response', {
        'message': fields.String(required=True)
    })
