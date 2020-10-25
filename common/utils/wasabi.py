#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
import boto3

# own modules
from app.settings.config import BaseConfig as Config

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def _connection(region=None):
    if region is None:
        s3 = boto3.client('s3',
                          endpoint_url='https://s3.wasabisys.com',
                          aws_access_key_id=Config.WASABI_ACCESS_KEY,
                          aws_secret_access_key=Config.WASABI_SECRET_ACCESS_KEY)
    else:
        s3 = boto3.client('s3',
                          endpoint_url='https://s3.wasabisys.com',
                          aws_access_key_id=Config.WASABI_ACCESS_KEY,
                          aws_secret_access_key=Config.WASABI_SECRET_ACCESS_KEY,
                          region=region)
    return s3


def create_bucket(bucket, region=None):
    if not bucket or str(bucket).strip().__eq__(''):
        return
    try:
        s3 = _connection(region=region)
        if region is None:
            s3.create_bucket(Bucket=bucket)
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration=location)
    except Exception as e:
        print(e.__str__())
        pass


def check_bucket_exist(bucket, region=None):
    try:
        s3 = _connection(region=region)
        response = s3.list_buckets()
        buckets = response['Buckets']
        for bk in buckets:
            if bucket.__eq__(bk['Name']):
                return True
        return False
    except Exception as e:
        print(e.__str__())
        return False


def upload_file(file_name, file, sub_folder, acl='public-read', bucket=Config.S3_BUCKET, object_name=None, region=None):
    if object_name is None:
        object_name = sub_folder + '/' + file_name
    s3 = _connection(region=region)
    try:
        if not check_bucket_exist(bucket=bucket, region=region):
            create_bucket(bucket=bucket, region=region)
        # location = 'https://s3.wasabisys.com/hoovada/'
        s3.upload_fileobj(
            file,
            bucket,
            object_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

        return object_name
    except Exception as e:
        print(e.__str__())
        return None


def delete_file(file_path, bucket=Config.S3_BUCKET, region=None):
    s3 = _connection(region=region)
    try:
        if not check_bucket_exist(bucket=bucket, region=region):
            create_bucket(bucket=bucket, region=region)
        # location = 'https://s3.wasabisys.com/hoovada/'
        s3.delete_object(Bucket=bucket, Key=file_path)

        return True
    except Exception as e:
        print(e.__str__())
        return False

# if __name__ == '__main__':
#     check_bucket_exist(bucket='hoovada')
