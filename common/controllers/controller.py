#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from abc import ABC

# third-party modules
from sqlalchemy.sql.expression import true
from flask import g, session

# own modules
from common.db import db
from common.utils.response import paginated_result, send_error
from app.constants import messages
from common.models.organization import Organization

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Controller(ABC):
    """ This class will control all interactions between clients, database server and other things"""
    
    query_classname = ''
    allowed_ordering_fields = []
    special_filtering_fields = ['from_date', 'to_date']

    def __repr__(self):
        if g.current_user:
            return "%s(%s)" % (self.query_classname, g.current_user.id)
        return "%s(guest)" % (self.query_classname)

    def get_model_class(self):
        return db.get_model(self.query_classname)

    def get_query(self):
        return self.get_model_class().query

    def get_query_results(self, params=None):
        if 'user_id' in params and params['user_id'] is not None: # add org params based on role in session
            params = self.add_org_data(params)
            print(params)
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
                    if filter_value is not None:
                        column_to_filter = getattr(self.get_model_class(), key)
                        if key == 'is_deleted' and column_to_filter and filter_value == true:
                            query = query.with_deleted()
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
        query = query.paginate(page, per_page, False)
        return query

    def create(self, *args, **kwargs):
        """
        Create object and insert to database.
        """
        pass

    def get(self, *args, **kwargs):
        """
        Return all objects from database
        """
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)

            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=e)


    def get_by_id(self, *args, **kwargs):
        """
        Get object from database by ID
        """
        pass

    def update(self, *args, **kwargs):
        """
        Updata object from search_data in database
        """
        pass

    def delete(self, *args, **kwargs):
        """
        Delete object from database.
        """
        pass

    def add_org_data(self, data):
        if data is None:
            data = {}
        if 'role' not in session:
            return data
        if session['role'] == 'user':
            data['entity_type'] = 'user'
        if session['role'] == 'organization' and 'organization_id' in session:
            data['entity_type'] = 'organization'
            data['organization_id'] = session['organization_id']
        return data
    
    def get_role_data(self):
        data = {
            'role': None,
            'organization_id': None
        }
        if 'role' in session:
            data['role'] = session['role']
        if 'organization_id' in session:
            data['organization_id'] = session['organization_id']
        return data
