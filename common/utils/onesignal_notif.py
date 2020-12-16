#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules

# third-party modules
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError

# own modules
from common.settings.config import CommonBaseConfig

client = Client(app_id=CommonBaseConfig.ONESIGNAL_APP_ID, 
    rest_api_key=CommonBaseConfig.ONESIGNAL_REST_API_KEY, 
    user_auth_key=CommonBaseConfig.ONESIGNAL_USER_AUTH_KEY)


def push_notif_to_specific_users(message, user_ids):
    try:
        notification_body = {
            'contents': {'en': message},
            'include_external_user_ids': user_ids,
        }

        # Make a request to OneSignal and parse response
        response = client.send_notification(notification_body)
        print(response.body) # JSON parsed response
        print(response.status_code) # Status code of response
        print(response.http_response) # Original http response object.

    except OneSignalHTTPError as e: # An exception is raised if response.status_code != 2xx
        print(e)
        print(e.status_code)
        print(e.http_response.json()) # You can see the details of error by parsing original response

def push_basic_notification(message):
    try:
        notification_body = {
            'contents': {'en': message},
            'included_segments': ['Subscribed Users'],
        }

        # Make a request to OneSignal and parse response
        response = client.send_notification(notification_body)
        print(response.body) # JSON parsed response
        print(response.status_code) # Status code of response
        print(response.http_response) # Original http response object.

    except OneSignalHTTPError as e: # An exception is raised if response.status_code != 2xx
        print(e)
        print(e.status_code)
        print(e.http_response.json()) # You can see the details of error by parsing original response