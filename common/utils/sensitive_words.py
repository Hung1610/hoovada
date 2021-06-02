#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from re import sub

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


sensitive_words = ['đu me', 'đủ mẹ', 'đủ má', 'chat sex', 'loạn luân', 'giao lưu sex', 'nc sex','chat xxx', 'phá trinh', 'tùm gái',
                   'childporn', 'bắn tinh', 'web sex','gái dâm', 'trai dâm', 'vãi đái', 'nứng lồn', 'quay tay', 
                   'kèo nhà cái', 'video sex', 'chat nude', 'nung lon', 'video xxx']


def is_sensitive(text, is_html=False):
    if text is None or str(text).strip().__eq__(''):
        return False
    
    try:
        if is_html is True:
            text = ' '.join(BeautifulSoup(text, "html.parser").stripped_strings)

        text = sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "",text).lower()
        for word in sensitive_words:
            if word in text:
                return True
        
        return False

    except Exception as e:
        raise e

        




