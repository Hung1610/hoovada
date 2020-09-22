#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app.modules.common.dto import Dto

# third-party modules
from flask_restx import marshal

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def send_result(data=None, message='OK', code=200, status=True):
    """ Send result if no error
    
    Args:
        data: The search_data to respond
        message (string): The message to respond
        code(int): The code of HTTP (2xx, 3xx, 4xx, 5xx)
        status (boolean): Status is true or false.
    
    Returns:
        (dict, int) -  The returned response contains search_data and code.
    `
        res = {
            'status': status,
            'code': code,
            'message': message,
            'data': data,
        }
    `
    """
    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code

def paginated_result(query=None, message='OK', code=200, status=True):
    res = {
        'status': status,
        'code': code,
        'message': message,
        'page': query.page,
        'page_count': query.pages,
        'data': query.items,
    }
    return res, code

def send_paginated_result(query=None, dto=None, message='OK', code=200, status=True):
    """ Send result if no error
    
    Args:
        query: The query to return
        message (string): The message to respond
        code(int): The code of HTTP (2xx, 3xx, 4xx, 5xx)
        status (boolean): Status is true or false.
    
    Returns:
        (dict, int) -  The returned response contains search_data and code.
    `
        res = {
            'status': status,
            'code': code,
            'message': message,
            'data': query,
        }
    `
    """
    res, code = paginated_result(query, message, code, status)
    res['data'] = marshal(res.get('data'), dto)
    return res, code


def send_error(data=None, message='Failed', code=400, status=False):
    """ Send result if error
    
    Args:
        data: The search_data to respond
        message (string): The message to respond
        code(int): The code of HTTP (2xx, 3xx, 4xx, 5xx)
        status (boolean): Status is true or false.
    
    Returns:
        (dict, int) -  The returned response contains search_data and code.
    `
        res = {
            'status': status,
            'code': code,
            'message': message,
            'data': data,
        } `
    """
    res = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code
