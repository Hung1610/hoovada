#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.models.answer import Answer, AnswerImprovement
from common.models.article import Article
from common.models.ban import UserBan
from common.models.bookmark import QuestionBookmark, AnswerBookmark, TopicBookmark
from common.models.comment import (AnswerComment, ArticleComment, PostComment,
                                   QuestionComment)
from common.models.favorite import (ArticleFavorite, ArticleCommentFavorite,
                                    AnswerFavorite, AnswerCommentFavorite, 
                                    PostFavorite,
                                    QuestionFavorite, QuestionCommentFavorite)
from common.models.follow import (UserFollow, TopicFollow)
from common.models.friend import UserFriend
from common.models.language import Language
from common.models.post import Post
from common.models.question import Question, QuestionProposal
from common.models.report import (ArticleCommentReport, AnswerCommentReport, ArticleReport,
                                  AnswerReport, PostReport, QuestionReport, TopicReport)
from common.models.reputation import Reputation
from common.models.share import (ArticleShare, AnswerShare, PostShare, QuestionShare,
                                    TopicShare)
from common.models.topic import Topic, TopicUserEndorse
from common.models.user import (User, SocialAccount, UserEducation, UserLanguage, UserLocation,
                                    UserTopic, UserEmployment, UserPermission,
                                    UserSeenQuestion, UserSeenArticle)
from common.models.vote import (ArticleVote, AnswerVote,
                                AnswerImprovementVote, PostVote,
                                QuestionVote)
from common.models.timeline import Timeline
from common.models.permission import Permission

# These tables/models will be ignored by Alembic/Flask-Migrate
from common.models.ignored import ApschedulerJobs

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."