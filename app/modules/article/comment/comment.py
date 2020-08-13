#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Comment(Model):
    __tablename__ = 'article_comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText)
    article_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

