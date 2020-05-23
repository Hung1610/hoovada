from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class AuthDto(Dto):
    name = 'auth'
    api = Namespace(name)
    model = api.model(name, {
        'display_name': fields.String(required=False),
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })

    # model_login = api.model(name, {
    #     'email': fields.String(required=True),
    #     'password': fields.String(requried=True)
    # })
