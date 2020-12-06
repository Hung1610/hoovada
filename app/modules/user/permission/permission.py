#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Permission(Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
