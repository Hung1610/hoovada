#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import os
import shutil
import uuid


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def directory_listing(folder_name, file_type=None):
    """ Listing all file in specific directory.

    Args:
        folder_name(string): The folder from which files are loaded.
        file_type: The specific kind of files to load.

    Returns:
    """
    if not folder_name or str(folder_name).__eq__(''):
        raise Exception("Folder must not be empty.")
    files = []
    allfiles = os.listdir(folder_name)
    for x in allfiles:
        # if os.path.isfile(folder_name+"/"+x):  # we need only file to return
        if not file_type:
            files.append(x)
        else:
            if str(x).endswith(file_type):
                files.append(x)
    return files


def file_info_gathering(filename):
    if not filename:
        raise Exception("The file name can not be empty")
    if not os.path.isfile(filename):
        raise Exception("The file" + filename + "does not exist or corrupt. Please check again.")
    info = os.stat(filename)
    return info


def get_file_name_extension(filename):
    # if not os.path.isfile(filename):
    #     raise Exception("Can not find the file. Check again please")
    splits = os.path.splitext(filename)
    name, ext = splits[0], splits[1]
    return name, ext


def copy_file(source_file, target_file):
    if not source_file:
        raise Exception("Check the input filename please. It can not be empty")
    if not os.path.isfile(source_file):
        raise Exception("File does not exist.")
    shutil.copy2(source_file, target_file)


def copy_directory(source_dir, target_dir):
    if not source_dir:
        raise Exception("Check the source directory name. It can not be empty.")
    if not target_dir:
        raise Exception("Check the destination directory name. It can not be empty.")
    shutil.move(source_dir, target_dir)


def copy_file_to_directory(source_file, target_dir):
    if not source_file:
        raise Exception("Check the source file name. It can not be empty.")
    if not target_dir:
        raise Exception("Check the destination directory name. It can not be empty.")
    shutil.move(source_file, target_dir)


def get_file_content(filename):
    """ Read content from file.
    Args:
        filename:
    
    Returns:
    """
    if not filename:
        return None
    with open(filename, mode='r') as file:
        content = file.read()
    return content


def generate_id():
    return uuid.uuid4().hex


def append_id(filename):
  return "{0}_{2}{1}".format(*os.path.splitext(filename) + (generate_id(),))

# filename = os.path.dirname(os.path.dirname(__file__))+"/data/zipfiles/Digi4-20180801.zip"
# infor = file_info_gathering(filename=filename)
# print(infor.st_mtime)

# name, ext = get_file_name_extension('D:\\file.txt')
# print(name, ext)

# if __name__ == '__main__':
#     import os
#     filename = os.path.dirname(os.path.dirname(__file__))+ "/data/anwendung/anwendung/Saveris2_180803_062438_3138.csv"
#     content = get_file_content(filename=filename)
#     print(content)
