#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

# third-party modules
from flask import current_app, url_for, g, request
from flask_restx import Api, Namespace, Resource

# own modules
from app.modules import *
from common.models import *
from common.utils.response import send_result
from common.tasks import test

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class HTTPSApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme='http')


ns_health = Namespace(name='health')
@ns_health.route('/')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes
        """
        
        test.send()
        return send_result(message="OK!", code=200)


ns_cache = Namespace(name='cache')
@ns_cache.route('/flush')
class Cache(Resource):
    def post(self):
        """ Use for Clearing cache
        """
        current_app.cache_context.clear()
        return send_result(message="Cache Cleared!", code=200)


def init_api():

    doc = False if environ.get('FLASK_ENV') == "production" else "/api/v1/openapi"

    api = HTTPSApi(title='Hoovada APIs',
                swagger='2.0',
                version='1.0',
                description='The Hoovada APIs',
                authorizations={
                    'apikey': {
                        'type': 'apiKey',
                        'in': 'header',
                        'name': 'X-API-KEY'
                    }
                },
                security='apikey',
                prefix='/api/v1',
                doc=doc)

    api.add_namespace(ns_health)
    api.add_namespace(ns_cache, '/cache')
    api.add_namespace(ns_auth, '/auth')
    api.add_namespace(ns_user, '/user')
    api.add_namespace(ns_user_education, '/user')
    api.add_namespace(ns_user_location, '/user')
    api.add_namespace(ns_user_topic, '/user')
    api.add_namespace(ns_user_language, '/user')
    api.add_namespace(ns_user_employment, '/user')
    api.add_namespace(ns_user_friend, '/user')
    api.add_namespace(ns_user_follow, '/user')
    api.add_namespace(ns_user_ban, '/user')
    api.add_namespace(ns_reputation, '/reputation')
    api.add_namespace(ns_topic, '/topic')
    api.add_namespace(ns_topic_follow, '/topic')
    api.add_namespace(ns_topic_bookmark, '/topic')
    api.add_namespace(ns_topic_report, '/topic')
    api.add_namespace(ns_topic_share, '/topic')
    api.add_namespace(ns_user_topic, '/user_topic')
    api.add_namespace(ns_post, '/post')
    api.add_namespace(ns_post_favorite, '/post')
    api.add_namespace(ns_post_vote, '/post')
    api.add_namespace(ns_post_report, '/post')
    api.add_namespace(ns_post_share, '/post')
    api.add_namespace(ns_post_comment, '/post')
    api.add_namespace(ns_article, '/article')
    api.add_namespace(ns_article_vote, '/article')
    api.add_namespace(ns_article_favorite, '/article')
    api.add_namespace(ns_article_report, '/article')
    api.add_namespace(ns_article_share, '/article')
    api.add_namespace(ns_article_comment, '/article')
    api.add_namespace(ns_article_comment_report, '/article/all/comment')
    api.add_namespace(ns_article_comment_vote, '/article/all/comment')
    api.add_namespace(ns_article_comment_favorite, '/article/all/comment')
    api.add_namespace(ns_question, '/question')
    api.add_namespace(ns_question_favorite, '/question')
    api.add_namespace(ns_question_share, '/question')
    api.add_namespace(ns_question_vote, '/question')
    api.add_namespace(ns_question_bookmark, '/question')
    api.add_namespace(ns_question_report, '/question')
    api.add_namespace(ns_question_comment, '/question')
    api.add_namespace(ns_question_comment_report, '/question/all/comment')
    api.add_namespace(ns_question_comment_vote, '/question/all/comment')
    api.add_namespace(ns_question_comment_favorite, '/question/all/comment')
    api.add_namespace(ns_answer, '/answer')
    api.add_namespace(ns_answer_improvement, '/answer')
    api.add_namespace(ns_answer_improvement_voting, '/answer/all/improvement')
    api.add_namespace(ns_answer_bookmark, '/answer')
    api.add_namespace(ns_answer_favorite, '/answer')
    api.add_namespace(ns_answer_report, '/answer')
    api.add_namespace(ns_answer_share, '/answer')
    api.add_namespace(ns_answer_vote, '/answer')
    api.add_namespace(ns_answer_comment, '/answer')
    api.add_namespace(ns_answer_comment_report, '/answer/all/comment')
    api.add_namespace(ns_answer_comment_vote, '/answer/all/comment')
    api.add_namespace(ns_answer_comment_favorite, '/answer/all/comment')
    api.add_namespace(ns_upload, '/file_upload')
    api.add_namespace(ns_search, '/search')
    api.add_namespace(ns_qa_timeline, '/timeline')
    api.add_namespace(ns_language, '/language')
    api.add_namespace(ns_permission, '/permission')
    api.add_namespace(ns_user_permission, '/user_permission')

    return api
