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

def push_notification():
    try:
        notification_body = {
            'contents': {'en': 'New notification'},
            'included_segments': ['Active Users'],
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