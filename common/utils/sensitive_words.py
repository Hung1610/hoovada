#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from re import sub

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


sensitive_words = ['du me', 'đu me', 'đủ mẹ', 'đủ má', 'đéo', 'địt', 'dâm đãng', 'làm tình',
                   'cuto', 'chat sex', 'loạn luân', 'giao lưu sex', 'nc sex', 'nc dâm',
                   'chat xxx', 'phá trinh', 'tùm gái', 'tìm trai', 'tìm bạn nữ', 
                   'childporn', 'bắn tinh', 'web sex', 'phim sex', 'film sex', 
                   'child porn','gái dâm', 'trai dâm', 'vãi đái', 'nứng lồn', 'quay tay', 
                   'kèo nhà cái', 'video sex', 'chat nude', 'nung lon', 
                   'video xxx', 'chát sex', 'ảnh sex']


def is_sensitive(text, is_html=False):
    if text is None or str(text).strip().__eq__(''):
        return False


    try:
        if is_html is True:
            text = ' '.join(BeautifulSoup(text, "html.parser").stripped_strings)

        for word in sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "",text):
            if word in text.lower():
                return True
        return False
    except Exception as e:
        raise e

        




