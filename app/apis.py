#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

# third-party modules
from flask import url_for
from flask_restx import Api, Namespace, Resource

# own modules
from app.modules import *
from app.modules.admin.career.career_view import api as ns_career
from common.utils.response import send_result
from common.cache import cache

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class HTTPSApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme=environ.get('WEB_PROTOCOL', 'https'))


ns_health = Namespace(name='healthz')


@ns_health.route('/')
class HealthCheck(Resource):
    def get(self):
        """ Use for Readiness and Liveness Probes"""
        return send_result(message="OK!", code=200)


ns_cache = Namespace(name='cache')


@ns_cache.route('/flush')
class Cache(Resource):
    def post(self):
        """ Use for Clearing cache"""
        cache.clear()
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
    api.add_namespace(ns_user_feed, '/user')
    api.add_namespace(ns_reputation, '/user')
    api.add_namespace(ns_topic, '/topic')
    api.add_namespace(ns_topic_bookmark, '/topic')
    api.add_namespace(ns_topic_report, '/topic')
    api.add_namespace(ns_topic_share, '/topic')
    api.add_namespace(ns_user_topic, '/user_topic')

    api.add_namespace(ns_post, '/post')
    api.add_namespace(ns_post_favorite, '/post')
    api.add_namespace(ns_post_report, '/post')
    api.add_namespace(ns_post_share, '/post')
    api.add_namespace(ns_post_comment, '/post')
    api.add_namespace(ns_post_comment_report, '/post/all/comment')
    api.add_namespace(ns_post_comment_favorite, '/post/all/comment')

    api.add_namespace(ns_article, '/article')
    api.add_namespace(ns_article_vote, '/article')
    api.add_namespace(ns_article_bookmark, '/article')
    api.add_namespace(ns_article_report, '/article')
    api.add_namespace(ns_article_share, '/article')
    api.add_namespace(ns_article_comment, '/article')
    api.add_namespace(ns_article_comment_report, '/article/all/comment')
    api.add_namespace(ns_article_comment_favorite, '/article/all/comment')

    api.add_namespace(ns_question, '/question')
    api.add_namespace(ns_question_share, '/question')
    api.add_namespace(ns_question_vote, '/question')
    api.add_namespace(ns_question_bookmark, '/question')
    api.add_namespace(ns_question_report, '/question')
    api.add_namespace(ns_question_comment, '/question')
    api.add_namespace(ns_question_comment_report, '/question/all/comment')
    api.add_namespace(ns_question_comment_favorite, '/question/all/comment')

    api.add_namespace(ns_answer, '/answer')
    api.add_namespace(ns_answer_improvement, '/answer')
    api.add_namespace(ns_answer_improvement_voting, '/answer/all/improvement')
    api.add_namespace(ns_answer_bookmark, '/answer')
    api.add_namespace(ns_answer_report, '/answer')
    api.add_namespace(ns_answer_share, '/answer')
    api.add_namespace(ns_answer_vote, '/answer')
    api.add_namespace(ns_answer_comment, '/answer')
    api.add_namespace(ns_answer_comment_report, '/answer/all/comment')
    api.add_namespace(ns_answer_comment_favorite, '/answer/all/comment')
    
    api.add_namespace(ns_upload, '/file')
    api.add_namespace(ns_search, '/search')
    api.add_namespace(ns_timeline, '/timeline')
    api.add_namespace(ns_language, '/language')
    api.add_namespace(ns_permission, '/permission')
    api.add_namespace(ns_user_permission, '/user_permission')

    api.add_namespace(ns_poll, '/poll')
    api.add_namespace(ns_poll_select, '/poll')
    api.add_namespace(ns_poll_topic, '/poll')
    api.add_namespace(ns_poll_user_select, '/poll/all/select')
    api.add_namespace(ns_poll_comment, '/poll')
    api.add_namespace(ns_poll_comment_favorite, '/poll/all/comment')
    api.add_namespace(ns_poll_comment_report, '/poll/all/comment')
    api.add_namespace(ns_poll_voting, '/poll')
    api.add_namespace(ns_poll_share, '/poll')
    api.add_namespace(ns_poll_report, '/poll')
    api.add_namespace(ns_poll_bookmark, '/poll')

    api.add_namespace(ns_career, '/admin/career')
    
    api.add_namespace(ns_organization, '/organization')
    api.add_namespace(ns_organization_user, '/organization')

    return api
