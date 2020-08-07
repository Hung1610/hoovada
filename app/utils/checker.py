#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from dateutil.parser import parse

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Checker:
    """ Checking type of object or something else
    """

    @staticmethod
    def is_date(date_str):
        """ Check if the string is date type

        Args 
            date_str(str): The string to check

        Returns:
            (boolean) True if the string is datetime format, and vise versa
        """
        try:
            parse(date_str)
            return True
        except:
            return False

    @staticmethod
    def is_numeric(number_str):
        """ Check if the string is numeric type

        Args:
            number_str(str): The String to check

        Returns
            (boolean) True if the string is numeric format, and vise versa
        """
        return str(number_str).isnumeric()
