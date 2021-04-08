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

# Update Messages
MSG_UPDATE_SUCCESS = '{} updated successfully.'
ERR_UPDATE_FAILED = 'Failed to update {}. Issue: {}!'

# Delete Messages
MSG_DELETE_SUCCESS = '{} deleted successful.'
ERR_DELETE_FAILED = 'Failed to delete {}. Issue: {}!'

# File Messages
ERR_NO_FILE = 'No file found in the request.'
ERR_FAILED_UPLOAD = 'Failed to upload file. Issue {}!'

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
ERR_USER_INAPPROPRIATE  = 'User information content is inappropriate!'
ERR_SPELLING = 'Please check spelling errors!'


########### Authentication Module #################

# common
ERR_NO_POLICY_ACCEPTED = "You need to accept the policy!"
ERR_NO_PASSWORD = "Please provide a password!"
ERR_NO_CONFIRMED_PASSWORD = "Please provide confirmed password!"
ERR_NO_DISPLAY_NAME = "Please provide a display name!"
ERR_NO_EMAIL = "Please provide an Email!"
ERR_INVALID_INPUT_EMAIL = "Email is not valid!"
ERR_INVALID_CONFIMED_PASSWORD = "The confirmed password is not correct!"
ERR_INVALID_INPUT_PASSWORD = "The password length must have at least 8!"
ERR_DISPLAY_NAME_EXISTED = "The display name '{}' has already existed!"
ERR_INCORRECT_EMAIL_OR_PASSWORD = "Email or password is incorrect!"
ERR_BANNED_ACCOUNT = "This account is banned!"
ERR_CODE_INCORRECT_EXPIRED = "The code is incorrect or expired!"
ERR_ACCOUNT_EXISTED = "The account with this email or number has already existed!"
ERR_ACCOUNT_NOT_REGISTERED = "Your account is not registered yet!"

ERR_REGISTRATION_FAILED = "Registration failed with issue {}!"
MSG_REGISTRATION_SUCCESS = "Account registration is successful."

ERR_RESET_PASSWORD_FAILED = "Password reset or change failed with issue {}!"
MSG_RESET_PASSWORD_SUCCESS = "Password reset or change is successful."
MSG_PASS_INPUT_PROMPT = "Please input a new password."

MSG_EMAIL_SENT = "Please check your Email."
MSG_PHONE_SENT = "Please check your phone message."

ERR_NO_TOKEN = "PLease provide a token!"

## Authentication
ERR_LOGIN_FAILED = "Failed to login!"
ERR_NOT_LOGIN = "You are not logged in!" 
MSG_LOGOUT_SUCESS = "Successfully logged out."
ERR_LOGOUT_FAILED = "Failed to log out with issue {}"

# Social login
ERR_SOCIAL_LOGIN_FAILED = "{} login failed with issue {}!"

# phone
ERR_INVALID_NUMBER = "Please provide a valid phone number!"
ERR_NO_PHONE_CODE = "Please provide a valid code!"
ERR_CHANGE_NUMBER_FAILED = "Changing phone number failed with issue {}!"
MSG_CHANGE_NUMBER_SUCCESS = "Changing phone number is successful."

########### Article Module #################

ERR_ARTICLE_ALREADY_EXISTS = 'Article with the title {} already exists!'
ERR_ARTICLE_SCHEDULED_BEFORE_CURRENT = 'Scheduled date is earlier than current time!'

########### Question Module #################
ERR_QUESTION_NOT_END_WITH_QUESION_MARK = 'Please end question title with question mark "?"!'
ERR_QUESTION_ALREADY_EXISTS = 'Question with the title {} already exists!'


########### Topics Module #################
ERR_TOPICS_MORE_THAN_5 = 'Number of topics more than 5!'
ERR_NOT_LOAD_TOPICS = 'Topics cannot be loaded!'


########### User Module #################
ERR_EMAIL_ALREADY_EXIST = 'The user with this email has existed!'
ERR_USER_PRIVATE_OR_DEACTIVATED = 'The user is either private or deactivated!'