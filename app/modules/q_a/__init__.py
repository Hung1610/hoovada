#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.modules.q_a.answer import api as ns_answer
from app.modules.q_a.answer.bookmark import api as ns_answer_bookmark
from app.modules.q_a.answer.comment import api as ns_answer_comment
from app.modules.q_a.answer.comment.favorite import \
    api as ns_answer_comment_favorite
from app.modules.q_a.answer.comment.report import \
    api as ns_answer_comment_report
from app.modules.q_a.answer.comment.voting import api as ns_answer_comment_vote
from app.modules.q_a.answer.favorite import api as ns_answer_favorite
from app.modules.q_a.answer.report import api as ns_answer_report
from app.modules.q_a.answer.share import api as ns_answer_share
from app.modules.q_a.answer.voting import api as ns_answer_vote
# own modules
from app.modules.q_a.question import api as ns_question
from app.modules.q_a.question.bookmark import api as ns_question_bookmark
from app.modules.q_a.question.comment import api as ns_question_comment
from app.modules.q_a.question.comment.favorite import \
    api as ns_question_comment_favorite
from app.modules.q_a.question.comment.report import \
    api as ns_question_comment_report
from app.modules.q_a.question.comment.voting import \
    api as ns_question_comment_vote
from app.modules.q_a.question.favorite import api as ns_question_favorite
from app.modules.q_a.question.report import api as ns_question_report
from app.modules.q_a.question.share import api as ns_question_share
from app.modules.q_a.question.voting import api as ns_question_vote
from app.modules.q_a.timeline import api as ns_qa_timeline

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."