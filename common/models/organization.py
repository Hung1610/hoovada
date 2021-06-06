#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

# third-party modules
from flask import g
from sqlalchemy.orm import backref
from sqlalchemy.sql import expression

# own modules
from common.db import db
from common.enum import OrganizationStatusEnum, OrganizationUserStatusEnum, EntityTypeEnum
from common.models.model import Model

Article = db.get_model('Article')

# Role org beside user role as normal
class OrganizationRole(object):
    @declared_attr
    def organization_id(cls):
        return db.Column(db.Integer,db.ForeignKey('organization.id', ondelete='CASCADE'), nullable=True, index=True)
    
    @declared_attr
    def organization(cls):
        return db.relationship("Organization",uselist=False, lazy=True)
    entity_type = db.Column(db.Enum(EntityTypeEnum, validate_strings=True),server_default="user", nullable=False, index=True)

class Organization(Model):
    """
    Define the Organization model.
    """
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Unicode(255), unique=True, nullable=False, index=True)  # , default='')
    website_url = db.Column(db.String(255), unique=True, nullable=True)
    phone_number = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255))  # (255), unique=True)
    logo_url = db.Column(db.String(255))  # (255), default='')
    description = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True) 
    user = db.relationship('User', uselist=False, lazy=True)
    status = db.Column(db.Enum(OrganizationStatusEnum, validate_strings=True), nullable=False, index=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def user_count(self):
        user_count = OrganizationUser.query.with_entities(db.func.count(OrganizationUser.id)).filter( \
            (OrganizationUser.organization_id == self.id) &
            (OrganizationUser.status == OrganizationUserStatusEnum.approved.name)).scalar()
        return user_count
    @property
    def is_joined_by_me(self):
        if g.current_user is not None and g.current_user.id is not None:
            current_user_id = g.current_user.id
            organization_user = OrganizationUser.query.filter_by(organization_id=self.id, user_id=current_user_id, status=OrganizationUserStatusEnum.approved.name).first()
            if organization_user is not None:
                return True
        return False
    
    @property
    def article_count(self):
        article_count = Article.query.with_entities(db.func.count(Article.id)).filter( \
            (Article.organization_id == self.id) &
            (Article.is_draft == expression.false()) &
            (Article.entity_type == EntityTypeEnum.organization.name)).scalar()
        return article_count


class OrganizationUser(Model):
    """
    Define the OrganizationUser model.
    """
    __tablename__ = 'organization_user'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id', ondelete='CASCADE'), nullable=False, index=True)
    organization = db.relationship('Organization', uselist=False, lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', uselist=False, lazy=True)
    status = db.Column(db.Enum(OrganizationUserStatusEnum, validate_strings=True), nullable=False, index=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)