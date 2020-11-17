#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
# bulit-in modules
import re
from datetime import datetime, timedelta
from io import StringIO

# third-party modules
from flask import current_app, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_mail import Message

# own modules
from common.utils.util import send_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def send_registered_user_emails_job():
    """ Send email notification to admin. Contains list of newly registered users

    Returns:
        None
    """
    db = current_app.db_context
    User = db.get_model('User')

    today_minus_one_week = datetime.now() - timedelta(weeks=1)
    users = User.query.filter(User.joined_date > today_minus_one_week).all()

    html = render_template('admin_registered_users_notification.html', users=users)
    for admin_email in current_app.config['MAIL_ADMINS']:
        send_email(admin_email, 'User Registered On Hoovada', html)

def add_jobs(scheduler):
    scheduler.add_job(send_registered_user_emails_job, trigger='interval', days=7)