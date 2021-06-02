#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from sqlalchemy.orm import backref
from sqlalchemy.sql import expression

# own modules
from common.db import db
from common.enum import CompanyStatusEnum, CompanyUserStatusEnum, OwnTypeEnum
from common.models.model import Model

Article = db.get_model('Article')

class Company(Model):
    """
    Define the Company model.
    """
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Unicode(255), unique=True, nullable=False, index=True)  # , default='')
    website_url = db.Column(db.String(255), unique=True, nullable=True)
    phone_number = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255))  # (255), unique=True)
    logo_url = db.Column(db.String(255))  # (255), default='')
    description = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True) 
    user = db.relationship('User', uselist=False, lazy=True)
    status = db.Column(db.Enum(CompanyStatusEnum, validate_strings=True), nullable=False, index=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def user_count(self):
        user_count = CompanyUser.query.with_entities(db.func.count(CompanyUser.id)).filter( \
            (CompanyUser.company_id == self.id) &
            (CompanyUser.status == CompanyUserStatusEnum.approved.name)).scalar()
        return user_count
    @property
    def is_joined_by_me(self):
        if g.current_user is not None and g.current_user.id is not None:
            current_user_id = g.current_user.id
            company_user = CompanyUser.query.filter_by(company_id=self.id, user_id=current_user_id, status=CompanyUserStatusEnum.approved.name).first()
            if company_user is not None:
                return True
        return False
    
    @property
    def article_count(self):
        article_count = Article.query.with_entities(db.func.count(Article.id)).filter( \
            (CompanyUser.company_id == self.id) &
            (Article.is_company_published == expression.true()) &
            (Article.own_type == OwnTypeEnum.company.name)).scalar()
        return article_count


class CompanyUser(Model):
    """
    Define the CompanyUser model.
    """
    __tablename__ = 'company_user'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=False, index=True)
    company = db.relationship('Company', uselist=False, lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', uselist=False, lazy=True)
    status = db.Column(db.Enum(CompanyUserStatusEnum, validate_strings=True), nullable=False, index=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)