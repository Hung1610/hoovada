

    #!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum
from datetime import datetime

# own modules
from common.db import db
from common.enum import BanTypeEnum
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ApschedulerJobs(Model):
    __tablename__ = 'apscheduler_jobs'
    __table_args__ = {'info': dict(is_view=True)}
