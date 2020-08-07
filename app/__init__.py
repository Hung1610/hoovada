#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource
from flask_restx import Namespace
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_restx import Api

# own modules
from app.utils.response import send_result
from app.settings.config import config_by_name
from app.modules import ns_auth, ns_user, ns_user_topic, ns_topic, ns_question_topic, ns_question, ns_answer, \
    ns_comment, ns_vote, ns_favorite, ns_share, ns_report, ns_upload, ns_search, ns_user_employment, ns_reputation


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'https' if '5000' in self.base_url else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

ns_health = Namespace(name='health')
@ns_health.route('/')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes
        
        Args:
            None

        Returns:
           200 code for success 
        """
        return send_result(message="OK!", code=200)



def init_app(config_name):
    app = Flask(__name__)
    # app.config['RESTFUL_JSON'] = {
    #     'ensure_ascii': False,
    #     'encoding':'utf8'
    # }
    app.config['JSON_AS_ASCII'] = False
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    return app


def init_api():
    api = MyApi(title='Hoovada APIs',
              version='1.0',
              description='The Hoovada APIs',
              authorizations=authorizations,
              security='apikey',
              doc='/api/v1/doc') #doc=False

    api.add_namespace(ns_auth, '/api/v1/auth')
    api.add_namespace(ns_user, '/api/v1/user')
    api.add_namespace(ns_user_employment, '/api/v1/user_employment')
    api.add_namespace(ns_reputation, '/api/v1/reputation')
    api.add_namespace(ns_topic, '/api/v1/topic')
    api.add_namespace(ns_user_topic, '/api/v1/user_topic')
    api.add_namespace(ns_question, '/api/v1/question')
    api.add_namespace(ns_question_topic, '/api/v1/question_topic')
    api.add_namespace(ns_answer, '/api/v1/answer')
    api.add_namespace(ns_comment, '/api/v1/comment')
    api.add_namespace(ns_vote, '/api/v1/vote')
    api.add_namespace(ns_favorite, '/api/v1/favorite')
    api.add_namespace(ns_share, '/api/v1/share')
    api.add_namespace(ns_report, '/api/v1/report')
    api.add_namespace(ns_upload, '/api/v1/file_upload')
    api.add_namespace(ns_search, '/api/v1/search')

    return api


def create_app(config):
    """ Create an app

    Args:
        config (dict)

    Returns:
        object - An initialized app
    """

    app = init_app(config_name=config)
    app.config.SWAGGER_UI_DOC_EXPANSION = 'none'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get", "post"]


    api = init_api()
    api.init_app(app)
    api.add_namespace(ns_health)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    
    return app
