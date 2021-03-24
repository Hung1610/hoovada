#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# Create Messages
MSG_CREATE_SUCCESS = '{} created successfully.'
MSG_CREATE_SUCCESS_WITH_ISSUE = '{} created partially successfully, but {}.'
MSG_ALREADY_EXISTS = '{} already exists!'
ERR_CREATE_FAILED = 'Failed to create {}. Issue: {}!'

# Get Messages
MSG_GET_SUCCESS = '{} get successfully.'
ERR_GET_FAILED = 'Failed to get {}. Issue: {}!'
ERR_LACKING_GET_PARAMS = 'Please provide {}!'

# Update Messages
MSG_UPDATE_SUCCESS = '{} updated successfully.'
ERR_UPDATE_FAILED = 'Failed to update {}. Issue: {}!'

# Delete Messages
MSG_DELETE_SUCCESS = '{} deleted successful.'
ERR_DELETE_FAILED = 'Failed to delete {}. Issue: {}!'

# File Messages
ERR_NO_FILE = 'No file found in the request.'

# General Errors
ERR_WRONG_DATA_FORMAT = 'Wrong data format!'
ERR_LACKING_QUERY_PARAMS = 'Query parameters not provided!'
ERR_PLEASE_PROVIDE = 'Please provide {}!'
ERR_NOT_FOUND = '{} not found!'
ERR_NOT_FOUND_WITH_ID = '{} not found with ID: {}!'
ERR_ISSUE = 'Issue: {}!'
ERR_NOT_AUTHORIZED = 'You have no authority to perform this action!'
ERR_CONTENT_TOO_SHORT = 'Content must be at least {} words!'

# Filtering content
ERR_TITLE_INAPPROPRIATE = 'Title content is inappropriate!'
ERR_BODY_INAPPROPRIATE  = 'Body content is inappropriate!'
ERR_SPELLING = 'Please check spelling errors!'

# Topics
ERR_TOPICS_MORE_THAN_5 = 'Number of topics more than 5!'
ERR_NOT_LOAD_TOPICS = 'Topics cannot be loaded!'

########### Authentication Module #################

# common
ERR_FAILED_REGISTER = "Failed to Register with the issue {}"
ERR_REGISTRATION_CONFIRMATION_FAILED = "Registration confirmation failed with issue {}!"

ERR_NO_TOKEN = "PLease provide access token!"

ERR_FAILED_LOGIN = "Failed to login. Please try again!"
ERR_BANNED_ACCOUNT = "This account is banned!"
ERR_CODE_INCORRECT_EXPIRED = "The code is incorrect or expired! Please access Hoovada.com to request for new code!"
ERR_CODE_FAILED_TO_SEND = "Failed to send code with issue {}!"

# Mail
## Registration
ERR_NO_POLICY_ACCEPTED = "You need to accept the policy!"
ERR_NO_PASSWORD = "Please provide a password!"
ERR_NO_CONFIRMED_PASSWORD = "Please provide confirmed password!"
ERR_NO_DISPLAY_NAME = "Please provide a display name!"
ERR_NO_EMAIL = "Please provide an Email!"
ERR_INVALID_INPUT_EMAIL = "Email is not valid!"
ERR_INVALID_CONFIMED_PASSWORD = "The confirmed password is not correct!"
ERR_INVALID_INPUT_PASSWORD = "The password length must have at least 8!"
ERR_EMAIL_EXISTED = "The Email {} has already existed, please log in!"
ERR_DISPLAY_NAME_EXISTED = "The display name {} has already existed!"
MSG_EMAIL_REGISTER_SUCCESS = "Please check your confirmation Email to complete the registration."
MSG_ACCOUNT_ACTIVATED = "Your account has been activated, please log in."

## Authentication
ERR_ACCOUNT_NOT_REGISTERED = "Your account is not registered yet!"
ERR_EMAIL_NOT_CONFIRMED = "Account is not confirmed. Please check your email to confirm the account!"
ERR_INCORRECT_EMAIL_OR_PASSWORD = "Email or password is incorrect!"
MSG_LOGOUT_SUCESS = "Successfully logged out."

# Social login
ERR_SOCIAL_LOGIN_FAILED = "{} login failed with issue {}!"


# phone
ERR_NO_PHONE = "Please provide a phone number!"
ERR_PHONE_INCORRECT = "The phone number format is incorrect!"
ERR_PHONE_ALREADY_EXISTED = "The phone number has already existed. Please log in!"
ERR_PHONE_NOT_REGISTERER = "The phone number {} is not registered. Please register!"
ERR_PHONE_NOT_CONFIRMED = "Account related to this phone number is not confirmed. Please check your message to confirm the account!"
ERR_PHONE_OR_PASS_INCORRECT = "The phone number or the password is incorrect!"
ERR_PHONE_NO_CODE = "Please provide phone code!"
MSG_PHONE_CODE_SENT = "Activation code has been sent to the phone number {}. Please check the message."
MSG_CODE_SENT = "Activation code has been sent. Please check your Email."
MSG_RESET_CODE_SENT = "Reset code has been sent. Please check your Email."
MSG_RESET_PASS_SUCCESS = "Password reset successfully. PLease input a new password."
MSG_OTP_SENT = "OTP has been sent."


########### Article Module #################

ERR_ARTICLE_ALREADY_EXISTS = 'Article with the title {} already exists!'
ERR_ARTICLE_SCHEDULED_BEFORE_CURRENT = 'Scheduled date is earlier than current time!'

########### Question Module #################
ERR_QUESTION_NOT_END_WITH_QUESION_MARK = 'Please end question title with question mark "?"!'
ERR_QUESTION_ALREADY_EXISTS = 'Question with the title {} already exists!'
