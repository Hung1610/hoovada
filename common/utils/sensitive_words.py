#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


sensitive_words = ['dm', 'du me', 'đu me', 'đủ mẹ', 'đủ má', 'đéo', 'địt', 'dâm đãng', 'làm tình',
                   'cuto', 'chat sex', 'loạn luân', 'dkm', 'giao lưu sex', 'nc sex', 'nc dâm',
                   'fuck ', 'chat xxx', 'sax', 'phá trinh', 'tùm gái', ' tìm trai', 'tìm bạn nữ', 'childporn', 'bắn tinh', 'việt cộng',
                   'web sex', 'phim sex', 'film sex', 'child porn', 'gái dâm', 'trai dâm', 'cặc', 'vãi đái',
                   'nứng lồn', 'quay tay', 'sục', 'kèo nhà cái', 'video sex', 'chat nude',
                   'casino online', 'nung lon', 'video xxx', 'vkl', 'lập group', 'chát sex', 'chơi casino', 'ảnh sex']


def check_sensitive(text):
    if text is None or str(text).strip().__eq__(''):
      return False

    result = False

    for word in sensitive_words:
        word = str(word).strip()
        if word.lower() in text.lower():
            result = True
            break

    return result

# if __name__ == '__main__':
#     print(sensitive_words.__len__())