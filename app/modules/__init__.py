#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.modules.article import (ns_article, ns_article_comment,
                                 ns_article_comment_favorite,
                                 ns_article_comment_report,
                                 ns_article_comment_vote, ns_article_favorite,
                                 ns_article_report, ns_article_share,
                                 ns_article_vote)
from app.modules.auth import api as ns_auth
from app.modules.file_upload import api as ns_upload
from app.modules.language import ns_language
from app.modules.post import (ns_post, ns_post_comment, ns_post_favorite,
                              ns_post_report, ns_post_share, ns_post_vote)
from app.modules.q_a import (
    ns_answer, ns_answer_bookmark, ns_answer_comment,
    ns_answer_comment_favorite, ns_answer_comment_report,
    ns_answer_comment_vote, ns_answer_favorite, ns_answer_report,
    ns_answer_share, ns_answer_vote, ns_qa_timeline, ns_question,
    ns_question_bookmark, ns_question_comment, ns_question_comment_favorite,
    ns_question_comment_report, ns_question_comment_vote, ns_question_favorite,
    ns_question_report, ns_question_share, ns_question_vote)
from app.modules.search import ns_search
from app.modules.topic import (ns_topic, ns_topic_bookmark, ns_topic_follow,
                               ns_topic_report, ns_topic_share)
# own modules
#from app.modules.user import api as ns_user, ns_user_employment, ns_reputation
from app.modules.user import (
    ns_user, ns_user_ban, ns_user_education, ns_user_follow, ns_user_friend,
    ns_user_language, ns_user_location, ns_user_topic)
from app.modules.user.permission import ns_permission
from app.modules.user.reputation import api as ns_reputation
from app.modules.user.user_employment import api as ns_user_employment
from app.modules.user.user_permission import ns_user_permission
from app.modules.user.user_view import api

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."
