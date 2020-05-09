from flask_restx import Resource
from flask_restx import Namespace

from .app import init_app, db
from .apis import init_api
from .utils.response import send_result

ns_hello = Namespace(name='hello')
api = init_api()


@ns_hello.route('')
class HelloHoovada(Resource):
    def get(self):
        """
        Testing the API

        :return the 'Hello Hoovada' text
        """
        return send_result(message="Hello Hoovada")


def init_hello():
    '''
    This is testing
    '''


def create_app(config):
    """
    Create an app

    :param: config

    :return: an initialized app
    """
    init_hello()
    app = init_app(config_name=config)
    api.init_app(app)
    api.add_namespace(ns_hello)
    return app
