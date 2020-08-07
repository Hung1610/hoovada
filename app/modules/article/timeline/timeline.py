#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class TimeLine(Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    activity = db.Column(db.String)
    activity_date = db.Column(db.Date)
    activity_time = db.Column(db.Time)
