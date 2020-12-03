#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
import hashlib
import re
from datetime import datetime, timedelta
from io import StringIO

# third-party modules
from flask_dramatiq import Dramatiq
from flask import current_app, g
from dramatiq import GenericActor

# own modules
from common.utils.util import send_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

dramatiq = Dramatiq()

@dramatiq.actor()
def test():
    print('THIS IS THE DEFAULT TASK MESSAGE')

@dramatiq.actor()
def update_seen_questions(question_id):
    db = current_app.db_context
    current_user = g.current_user
    UserSeenQuestion = db.get_model('UserSeenQuestion')

    seen_count = UserSeenQuestion.query.with_entities(db.func.count(UserSeenQuestion.id)).filter(UserSeenQuestion.user_id == current_user.id\
        & UserSeenQuestion.question_id == question_id).scalar()

@dramatiq.actor()
def update_seen_articles(article_id):
    db = current_app.db_context
    current_user = g.current_user
    UserSeenArticle = db.get_model('UserSeenArticle')

    seen_count = UserSeenArticle.query.with_entities(db.func.count(UserSeenArticle.id)).filter(UserSeenArticle.user_id == current_user.id\
        & UserSeenArticle.article_id == article_id).scalar()