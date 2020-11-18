#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

# built-in modules
from app.app import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Controller(ABC):
    """
    This class will control all interactions between clients, database server and other things.
    """
    query_classname = ''
    allowed_ordering_fields = []
    special_filtering_fields = ['from_date', 'to_date']

    def get_model_class(self):
        return db.get_model(self.query_classname)

    def get_query(self):
        return self.get_model_class().query

    def get_query_results(self, params=None):
        query = self.get_query()
        if params:
            ordering_fields_asc, ordering_fields_desc = params.pop('order_by_asc', None), params.pop('order_by_desc', None)
            page, per_page = params.pop('page', None), params.pop('per_page', None)
            query = self.apply_filtering(query, params)
            query = self.apply_sorting(query, ordering_fields_desc, ordering_fields_asc)
            query = self.apply_pagination(query, page, per_page)

        return query

    def get_query_results_count(self, params=None):
        return self.get_query_results(params).total

    def apply_filtering(self, query, params):
        if params:
            for key in params:
                if not key in self.special_filtering_fields:
                    filter_value = params[key]
                    if filter_value:
                        column_to_filter = getattr(self.get_model_class(), key)
                        if key == 'is_deleted':
                            if column_to_filter:
                                query = query.filter(not column_to_filter)
                            else:
                                query = query.filter(column_to_filter)
                        elif column_to_filter:
                            query = query.filter(column_to_filter == filter_value)

        return query

    def apply_sorting(self, query, ordering_fields_desc=None, ordering_fields_asc=None):
        if ordering_fields_desc:
            for ordering_field in ordering_fields_desc:
                if ordering_field in self.allowed_ordering_fields:
                    column_to_sort = getattr(self.get_model_class(), ordering_field)
                    query = query.order_by(db.desc(column_to_sort))

        if ordering_fields_asc:
            for ordering_field in ordering_fields_asc:
                if ordering_field in self.allowed_ordering_fields:
                    column_to_sort = getattr(self.get_model_class(), ordering_field)
                    query = query.order_by(db.asc(column_to_sort))

        return query
    
    def apply_pagination(self, query, page=1, per_page=10):
        query = query.paginate(page, per_page)
        return query

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Create object and insert to database.
        """
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        """
        Return all objects from database
        """
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        """
        Get object from database by ID
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Updata object from search_data in database
        """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Delete object from database.
        """
        pass
