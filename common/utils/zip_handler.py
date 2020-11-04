#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# built-in
import zipfile

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def unzip_file(filename, path_to_extract):
    if not filename:
        raise Exception("The " + filename.__str__ + " doest not exist. Please check again.")
    if not os.path.isfile(filename):
        raise Exception("File doest not exist. Please check again.")
    zip = zipfile.ZipFile(file=filename, mode='r')
    zip.extractall(path=path_to_extract)
    zip.close()


def test_unzip():
    import os
    filename = os.path.dirname(os.path.dirname(__file__))+'/data/zipfiles/Digi4-20180801.zip'
    path_to_extract = os.path.dirname(os.path.dirname(__file__))+'/data/zipfiles/csv'
    try:
        unzip_file(filename=filename, path_to_extract=path_to_extract)
    except:
        print('Could not extract zip file')

if __name__ == '__main__':
    test_unzip()