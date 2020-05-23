from flask_restx import Api

from app.modules import ns_auth, ns_user, ns_user_topic, ns_topic, ns_question_topic, ns_question, ns_answer, ns_comment

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
              security='apikey'
              )
    api.add_namespace(ns_auth, '/api/v1/auth')
    api.add_namespace(ns_user, '/api/v1/user')
    api.add_namespace(ns_topic, '/api/v1/topic')
    api.add_namespace(ns_user_topic, '/api/v1/user_topic')
    api.add_namespace(ns_question, '/api/v1/question')
    api.add_namespace(ns_question_topic, '/api/v1/question_topic')
    api.add_namespace(ns_answer, '/api/v1/answer')
    # api.add_namespace(ns_comment, '/api/v1/comment')

    return api
