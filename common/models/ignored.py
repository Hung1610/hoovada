

    #!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules

# own modules
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# Define all tables that you want Flask Migrate/Alembic to ignore
# while creating migrations, upgrading the database


class ApschedulerJobs(Model):
    __tablename__ = 'apscheduler_jobs'
    __table_args__ = {'info': dict(is_view=True)}
