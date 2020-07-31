#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app.modules.user import api as ns_user
from app.modules.auth import api as ns_auth
from app.modules.q_a import ns_question, ns_answer, ns_comment, ns_vote, ns_favorite, ns_share, ns_report
from app.modules.topic import ns_topic, ns_user_topic, ns_question_topic
from app.modules.file_upload import api as ns_upload
from app.modules.search import ns_search
from app.modules.user.user_view import api

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."
