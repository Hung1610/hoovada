#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from dateutil.parser import parse

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Checker:
    """
    Class Checker is a util for checking type of object or something else
    """

    @staticmethod
    def is_date(date_str):
        """
        Check if the string is date type

        :param date_str: The string to check

        :return: True if the string is datetime format, and vise versa
        """
        try:
            parse(date_str)
            return True
        except:
            return False

    @staticmethod
    def is_numeric(number_str):
        """
        Check if the string is numeric type

        :param number_str: The String to check

        :return: True if the string is numeric format, and vise versa
        """
        return str(number_str).isnumeric()
