#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# q,a and article only has vote while post or comment only has favorite
from app.modules.article import (ns_article, 
                                 ns_article_comment,
                                 ns_article_comment_favorite,
                                 ns_article_comment_report,
                                 ns_article_report, 
                                 ns_article_share,
                                 ns_article_vote, 
                                 ns_article_bookmark)

from app.modules.q_a import ( ns_answer,
                              ns_answer_report,
                              ns_answer_share, 
                              ns_answer_vote,
                              ns_answer_bookmark, 
                              ns_answer_improvement, 
                              ns_answer_improvement_voting,
                              ns_answer_comment,
                              ns_answer_comment_favorite, 
                              ns_answer_comment_report,

                              ns_question,
                              ns_question_bookmark, 
                              ns_question_report, 
                              ns_question_share, 
                              ns_question_vote,
                              ns_question_comment, 
                              ns_question_comment_favorite,
                              ns_question_comment_report)

from app.modules.post import (ns_post,
                              ns_post_report, 
                              ns_post_favorite,
                              ns_post_share,
                              ns_post_comment, 
                              ns_post_comment_favorite,
                              ns_post_comment_report)

from app.modules.topic import (ns_topic, 
                               ns_topic_bookmark,
                               ns_topic_report, 
                               ns_topic_share)

from app.modules.user import (ns_user, 
                              ns_user_ban, 
                              ns_user_education, 
                              ns_user_follow, 
                              ns_user_friend,
                              ns_user_language, 
                              ns_user_location, 
                              ns_user_topic,
                              ns_user_feed)

from app.modules.user.permission import ns_permission
from app.modules.user.reputation import api as ns_reputation
from app.modules.user.user_employment import api as ns_user_employment
from app.modules.user.user_permission import ns_user_permission
from app.modules.user.user_view import api
from app.modules.auth import api as ns_auth
from app.modules.file_upload import api as ns_upload
from app.modules.language import ns_language
from app.modules.search import ns_search
from app.modules.timeline import ns_timeline
from app.modules.poll import ns_poll
from app.modules.poll.poll_select import ns_poll_select
from app.modules.poll.poll_topic import ns_poll_topic
from app.modules.poll.poll_user_select import ns_poll_user_select
from app.modules.poll import (ns_poll_comment, ns_poll_comment_favorite, ns_poll_comment_report, ns_poll_voting, ns_poll_share, ns_poll_report,ns_poll_bookmark)

