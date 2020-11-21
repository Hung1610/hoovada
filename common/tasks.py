#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
import hashlib
import re
from datetime import datetime, timedelta
from io import StringIO

# third-party modules
from flask_dramatiq import Dramatiq
from flask import current_app, g
from dramatiq import GenericActor

# own modules
from common.utils.util import send_email
from dramatiq_queue import rabbitmq_broker

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

dramatiq = Dramatiq()

@dramatiq.actor()
def test():
    print('TEST SUCCESS')