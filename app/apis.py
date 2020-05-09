from flask_restx import Api

from app.modules import ns_auth, ns_user, ns_user_topic

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


def init_api():
    api = Api(title='Hoovada APIs',
              version='0.1',
              description='The Hoovada APIs',
              authorizations=authorizations,
              security='apikey')
    api.add_namespace(ns_auth, '/api/v1/auth')
    api.add_namespace(ns_user, '/api/v1/user')
    api.add_namespace(ns_user_topic, '/api/v1/user_topic')
    return api
