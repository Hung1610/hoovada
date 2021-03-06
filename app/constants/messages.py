#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


########### Common messages #################
ERR_FAILED_UPLOAD = 'Failed to upload file. Issue {}!'
ERR_CREATE_FAILED = 'Failed to create. Issue: {}!'
ERR_GET_FAILED = 'Failed to get. Issue: {}!'
ERR_UPDATE_FAILED = 'Failed to update. Issue: {}!'
ERR_DELETE_FAILED = 'Failed to delete. Issue: {}!'
ERR_WRONG_DATA_FORMAT = 'Wrong data format!'
ERR_PLEASE_PROVIDE = 'Please provide {}!'
ERR_NOT_FOUND_WITH_ID = '{} not found with ID: {}!'
ERR_ISSUE = 'Issue: {}!'
ERR_NOT_ALLOWED_PARAMS = 'The parameter {} is not allowed!'
ERR_NOT_AUTHORIZED = 'You have no authority to perform this action!'
ERR_TITLE_INAPPROPRIATE = 'Title content is inappropriate!'
ERR_BODY_INAPPROPRIATE  = 'Body content is inappropriate!'
ERR_USER_INAPPROPRIATE  = 'User information content is inappropriate!'
ERR_ALREADY_EXISTS = 'Already exists!'
ERR_NOT_FOUND = 'Not found!'
ERR_FIXED_TOPIC_NOT_FOUND = 'Fixed topic not found!'
ERR_FAVORITE_NOT_ALLOWED = 'Favorite not allowed!'
ERR_VOTING_NOT_ALLOWED = 'Voting not allowed!'
ERR_COMMENT_NOT_ALLOWED = 'Comment not allowed!'

########### Authentication Module #################

# common
ERR_NO_POLICY_ACCEPTED = "You need to accept the policy!"
ERR_INVALID_INPUT_EMAIL = "Email is not valid!"
ERR_INVALID_CONFIMED_PASSWORD = "The confirmed password is not correct!"
ERR_INVALID_INPUT_PASSWORD = "The password length must have at least 8!"
ERR_DISPLAY_NAME_EXISTED = "The display name has already existed!"
ERR_INCORRECT_EMAIL_OR_PASSWORD = "Email or password is incorrect!"
ERR_BANNED_ACCOUNT = "This account is banned!"
ERR_CODE_INCORRECT_EXPIRED = "The code is incorrect or expired!"
ERR_ACCOUNT_EXISTED = "The account with this email or number has already existed!"
ERR_ACCOUNT_NOT_REGISTERED = "Your account is not registered yet!"

ERR_REGISTRATION_FAILED = "Registration failed with issue {}!"
ERR_RESET_PASSWORD_FAILED = "Password reset or change failed with issue {}!"
MSG_EMAIL_SENT = "Please check your Email."
MSG_PHONE_SENT = "Please check your phone message."

## Authentication
ERR_NOT_LOGIN = "You are not logged in!" 
ERR_LOGOUT_FAILED = "Failed to log out with issue {}"

# Social login
ERR_SOCIAL_LOGIN_FAILED = "Social login failed with issue {}!"

# phone
ERR_INVALID_NUMBER = "Please provide a valid phone number!"
ERR_CHANGE_NUMBER_FAILED = "Changing phone number failed with issue {}!"

########### Article Module #################

ERR_ARTICLE_SCHEDULED_BEFORE_CURRENT = 'Scheduled date is earlier than the current time!'

########### Question Module #################
ERR_QUESTION_NOT_END_WITH_QUESION_MARK = 'Please end question title with question mark!'

########### Answer Module #################
ERR_USER_ALREADY_ANSWERED = 'Already answered this question!'
ERR_USER_INFO_MORE_THAN_1 = 'More than 1 user information is selected!'
ERR_ANSWER_AUDIO_ALLOWED = 'Question does not allow to answer by audio!'
ERR_ANSWER_VIDEO_ALLOWED = 'Question does not allow to answer by video!'

########### User Module #################
ERR_EMAIL_ALREADY_EXIST = 'The user with this email has existed!'
ERR_USER_PRIVATE_OR_DEACTIVATED = 'The user is either private or deactivated!'
ERR_SEND_REQUEST_TO_ONESELF = 'Sending request to oneself!'