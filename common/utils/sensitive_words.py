#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                   'video xxx', 'chát sex', 'chơi casino', 'ảnh sex']


def check_sensitive(text):
    if text is None or str(text).strip().__eq__(''):
      return False

    result = False

    for word in sensitive_words:
        word = str(word).strip()
        if word.lower() in text.lower():
            result = True
            print(word.lower())

    return result

#if __name__ == '__main__':
  #print(sensitive_words.__len__())