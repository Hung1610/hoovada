sensitive_words = ['lồn', 'dm', 'du me', 'đu me', 'đủ mẹ', 'đủ má', ' đù', 'đụ', 'đéo', 'dái', 'địt', 'vãi', 'cu', 'dâm đãng', 'làm tình',
                   'cuto', 'chat sex', 'loạn luân', 'slm', 'dkm', 'porn', 'dú', 'bú', 'giao lưu sex', 'nc sex', 'xxx',
                   'fuck ', 'chat xxx', 'sax', 'phá trinh', 'tùm gái', ' tìm trai', 'tìm bạn nữ', 'childporn',
                   'trai bao', 'gái bao', 'web sex', 'phim sex', 'film sex', 'child porn', 'gái dâm', 'trai dâm',
                   'nứng', 'some nam nữ', 'sex trẻ em', 'quay tay', 'zl', 'sục', 'zalo', 'kèo nhà cái', 'soi kèo',
                   'casino online', 'nung lon', 'video sex']


def check_sensitive(text):
    if text is None or str(text).strip().__eq__(''):
        return True
    result = False
    for word in sensitive_words:
        word = str(word).strip()
        if word in text or str(word).upper() in text or str(word).lower() in text:
            result = True
            break
    return result

# if __name__ == '__main__':
#     print(sensitive_words.__len__())