#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
