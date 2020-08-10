#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Api
from flask import url_for

# own modules
from app.modules import ns_auth, ns_user, ns_user_topic, ns_topic, ns_question_topic, ns_question, ns_answer, \
    ns_comment, ns_vote, ns_favorite, ns_share, ns_report, ns_upload, ns_search, ns_user_employment, ns_reputation,\
    ns_article

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


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
        #if '80' in self.base_url or '443' in self.base_url:
        #    scheme = 'https'
        #else:
        #    scheme = 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

def init_api(mode):

    doc = False if mode == "prod" else "/api/v1/doc"

    api = MyApi(title='Hoovada APIs',
                swagger='2.0',
                version='1.0',
                description='The Hoovada APIs',
                authorizations=authorizations,
                security='apikey',
                doc=doc)

    api.add_namespace(ns_auth, '/api/v1/auth')
    api.add_namespace(ns_user, '/api/v1/user')
    api.add_namespace(ns_user_employment, '/api/v1/user_employment')
    api.add_namespace(ns_reputation, '/api/v1/reputation')
    api.add_namespace(ns_topic, '/api/v1/topic')
    api.add_namespace(ns_article, '/api/v1/article')
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
