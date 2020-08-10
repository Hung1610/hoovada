#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.modules.common.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Favorite(Model):
    __tablename__ = 'article_favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'),
        nullable=False)
    article = db.relationship('Article', backref='article_favorites', lazy=True) # one-to-many relationship with table Article
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
