#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
#from app.modules.user import api as ns_user, ns_user_employment, ns_reputation
from app.modules.user import ns_user,\
                            ns_user_education, ns_user_location, ns_user_topic, ns_user_language
from app.modules.auth import api as ns_auth
from app.modules.q_a import ns_question, ns_question_vote, ns_question_favorite, ns_question_share, ns_question_report, ns_question_bookmark,\
                            ns_answer, ns_answer_bookmark, ns_answer_favorite, ns_answer_report, ns_answer_share, ns_answer_vote,\
                            ns_answer_comment, ns_answer_comment_report, ns_answer_comment_vote, ns_answer_comment_favorite,\
                            ns_question_comment, ns_question_comment_report, ns_question_comment_vote, ns_question_comment_favorite,\
                            ns_qa_timeline,\
                            ns_comment, ns_comment_report, ns_comment_vote
from app.modules.article import ns_article, ns_article_vote, ns_article_favorite, ns_article_report, ns_article_share, ns_article_comment
from app.modules.topic import ns_topic, ns_question_topic, ns_topic_bookmark, ns_topic_report, ns_topic_share
from app.modules.file_upload import api as ns_upload
from app.modules.search import ns_search
from app.modules.user.user_view import api
from app.modules.user.user_employment import api as ns_user_employment
from app.modules.user.reputation import api as ns_reputation
from app.modules.language import ns_language


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."
