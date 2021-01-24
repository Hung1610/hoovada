#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from sqlalchemy import event

# own modules
from common.db import db
from common.enum import VotingStatusEnum
from common.models.mixins import AuditCreateMixin, AuditUpdateMixin
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Reputation(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'reputation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table User
    score = db.Column(db.Float)
