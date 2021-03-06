#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.modules.post.post_view import api as ns_post
from app.modules.post.favorite.favorite_view import api as ns_post_favorite
from app.modules.post.report.report_view import api as ns_post_report
from app.modules.post.share.share_view import api as ns_post_share

from app.modules.post.comment.comment_view import api as ns_post_comment
from app.modules.post.comment.favorite import api as ns_post_comment_favorite
from app.modules.post.comment.report import api as ns_post_comment_report

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."