#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Api
from flask import url_for

# own modules
from app.modules import ns_auth, ns_user, ns_user_topic, ns_topic, ns_question_topic, ns_question, ns_answer, \
    ns_comment, ns_vote, ns_favorite, ns_share, ns_report, ns_upload, ns_search, ns_user_employment, ns_reputation,\
    ns_article, ns_article_vote, ns_article_favorite, ns_article_report, ns_article_share, ns_article_comment

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

class HTTPSApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme='http')

def init_api(mode):

    doc = False if mode == "prod" else "/api/v1/doc"

    api = HTTPSApi(title='Hoovada APIs',
                swagger='2.0',
                version='1.0',
                description='The Hoovada APIs',
                authorizations=authorizations,
                security='apikey',
                prefix='/api/v1',
                doc=doc)

    api.add_namespace(ns_auth, '/auth')
    api.add_namespace(ns_user, '/user')
    api.add_namespace(ns_user_employment, '/user_employment')
    api.add_namespace(ns_reputation, '/reputation')
    api.add_namespace(ns_topic, '/topic')
    api.add_namespace(ns_article, '/article')
    api.add_namespace(ns_article_vote, '/article')
    api.add_namespace(ns_article_favorite, '/article')
    api.add_namespace(ns_article_report, '/article')
    api.add_namespace(ns_article_share, '/article')
    api.add_namespace(ns_article_comment, '/article')
    api.add_namespace(ns_user_topic, '/user_topic')
    api.add_namespace(ns_question, '/question')
    api.add_namespace(ns_question_topic, '/question_topic')
    api.add_namespace(ns_answer, '/answer')
    api.add_namespace(ns_comment, '/comment')
    api.add_namespace(ns_vote, '/vote')
    api.add_namespace(ns_favorite, '/favorite')
    api.add_namespace(ns_share, '/share')
    api.add_namespace(ns_report, '/report')
    api.add_namespace(ns_upload, '/file_upload')
    api.add_namespace(ns_search, '/search')

    return api
