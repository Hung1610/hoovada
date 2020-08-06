#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class SearchableMixin(object):

    @classmethod
    def search(cls, query, page_number, per_page):
        # ids, total = query_index(cls.__tablename__, query, page_number, per_page)
        pass

    @classmethod
    def before_commit(cls, session):
        pass

    @classmethod
    def after_commit(cls, session):
        pass



