#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleTopic(Model):
    __tablename__ = 'topic_article'
    __table_args__ = { "info": dict(is_view=True)}

    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
