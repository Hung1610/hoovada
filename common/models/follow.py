#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from common.db import db
from common.models.model import Model
from common.enum import EntityTypeEnum
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseFollow(OrganizationRole):
    id = db.Column(db.Integer, primary_key=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserFollow(Model, BaseFollow):
    __tablename__ = 'user_follow'
    
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), index=True)
    follower = db.relationship('User', foreign_keys=[follower_id], lazy=True) # one-to-many relationship with table User
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    followed = db.relationship('User', foreign_keys=[followed_id], lazy=True) # one-to-many relationship with table User