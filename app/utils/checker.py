#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from dateutil.parser import parse

# third-party modules
import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer, HTMLChunker, EmailFilter, URLFilter

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


en_dict = enchant.Dict("en_US")
vi_dict = enchant.Dict("vi_VN")


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

def check_spelling(text, lang=["en_US", "vi_VN"]):
    tknzr = get_tokenizer("en_US")              # Using en_US, it's the most general tokenizer
    # Check for errors in tokenized text
    errors = []
    for word in tknzr(text, [EmailFilter, URLFilter], chunkers=(HTMLChunker,)):
        if not (vi_dict.check(word) and en_dict.check(word)):
            errors.append({"error": word, "suggestion": vi_dict.suggest(word)[:5] + en_dict.suggest(word)[:5]})

    return errors
