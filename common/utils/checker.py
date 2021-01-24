#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import enchant
# built-in modules
from dateutil.parser import parse
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, HTMLChunker, URLFilter, get_tokenizer

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

b = enchant.Broker()
b.set_ordering("*","aspell,hunspell")

en_dict = enchant.Dict("en_US")
vi_dict = enchant.Dict("vi_VN")


class Checker:
    """ Checking type of object
    """

    @staticmethod
    def is_date(date_str):
        """ Check if the string is date type"""
        try:
            parse(date_str)
            return True
        except:
            return False

    @staticmethod
    def is_numeric(number_str):
        """ Check if the string is numeric type"""
        return str(number_str).isnumeric()

def check_spelling(text):
    tknzr = get_tokenizer("en_US", filters=[EmailFilter, URLFilter], chunkers=(HTMLChunker,))              # Using en_US, it's the most general tokenizer
    # Check for errors in tokenized text
    errors = []
    for word in tknzr(text):
        if (not vi_dict.check(word[0])) and (not en_dict.check(word[0])):
            errors.append({"error": word[0], "suggestion": vi_dict.suggest(word[0])[:5] + en_dict.suggest(word[0])[:5]})

    return errors
