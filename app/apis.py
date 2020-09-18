#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Api
from flask import url_for

# own modules
from app.modules import ns_auth, ns_user, ns_topic, ns_question_topic, ns_question, ns_answer, \
    ns_question_vote, ns_question_favorite, ns_question_share, ns_question_report, \
    ns_question_comment, ns_question_comment_report, ns_question_comment_vote,\
    ns_upload, ns_search, ns_user_employment, ns_reputation,\
    ns_article, ns_article_vote, ns_article_favorite, ns_article_report, ns_article_share, ns_article_comment,\
    ns_qa_timeline, ns_question_bookmark, ns_topic_bookmark,\
    ns_comment_report, ns_comment_vote,\
    ns_answer_bookmark, ns_answer_favorite, ns_answer_report, ns_answer_share, ns_answer_vote,\
    ns_answer_comment, ns_answer_comment_report, ns_answer_comment_vote,\
    ns_user_education, ns_user_location, ns_user_topic, ns_user_language,\
    ns_language

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
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

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
    api.add_namespace(ns_user_education, '/user')
    api.add_namespace(ns_user_location, '/user')
    api.add_namespace(ns_user_topic, '/user')
    api.add_namespace(ns_user_language, '/user')
    api.add_namespace(ns_user_employment, '/user_employment')
    api.add_namespace(ns_reputation, '/reputation')
    api.add_namespace(ns_topic, '/topic')
    api.add_namespace(ns_topic_bookmark, '/topic')
    api.add_namespace(ns_user_topic, '/user_topic')
    api.add_namespace(ns_article, '/article')
    api.add_namespace(ns_article_vote, '/article')
    api.add_namespace(ns_article_favorite, '/article')
    api.add_namespace(ns_article_report, '/article')
    api.add_namespace(ns_article_share, '/article')
    api.add_namespace(ns_article_comment, '/article')
    api.add_namespace(ns_question, '/question')
    api.add_namespace(ns_question_favorite, '/question')
    api.add_namespace(ns_question_share, '/question')
    api.add_namespace(ns_question_vote, '/question')
    api.add_namespace(ns_question_bookmark, '/question')
    api.add_namespace(ns_question_report, '/question')
    api.add_namespace(ns_question_topic, '/question_topic')
    api.add_namespace(ns_question_comment, '/question')
    api.add_namespace(ns_question_comment_report, '/question/all/comment')
    api.add_namespace(ns_question_comment_vote, '/question/all/comment')
    api.add_namespace(ns_answer, '/answer')
    api.add_namespace(ns_answer_bookmark, '/answer')
    api.add_namespace(ns_answer_favorite, '/answer')
    api.add_namespace(ns_answer_report, '/answer')
    api.add_namespace(ns_answer_share, '/answer')
    api.add_namespace(ns_answer_vote, '/answer')
    api.add_namespace(ns_answer_comment, '/answer')
    api.add_namespace(ns_answer_comment_report, '/answer/all/comment')
    api.add_namespace(ns_answer_comment_vote, '/answer/all/comment')
    api.add_namespace(ns_upload, '/file_upload')
    api.add_namespace(ns_search, '/search')
    api.add_namespace(ns_qa_timeline, '/timeline')
    api.add_namespace(ns_language, '/language')

    return api
