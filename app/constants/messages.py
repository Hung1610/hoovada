#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# # Create Messages
MSG_CREATE_SUCCESS = '{} created successful.'
MSG_CREATE_SUCCESS_WITH_ISSUE = '{} created partially successful, but {}.'
MSG_ALREADY_EXISTS = '{} already exists.'
ERR_CREATE_FAILED = 'Failed to create {}. Issue: {}'

# # Get Messages
MSG_GET_SUCCESS_SUCCESS = '{} get successful.'
ERR_GET_FAILED = 'Failed to get {}. Issue: {}'
ERR_LACKING_GET_PARAMS = 'Please provide {}.'

# # Get Single/Update Messages
MSG_UPDATE_SUCCESS = '{} updated successful.'
ERR_UPDATE_FAILED = 'Failed to update {}. Issue: {}'

# # Delete Messages
MSG_DELETE_SUCCESS = '{} deleted successful.'
ERR_DELETE_FAILED = 'Failed to delete {}.'

# # File Messages
ERR_NO_FILE = 'No file found in the request.'

# # General Errors
ERR_WRONG_DATA_FORMAT = 'Wrong data format.'
ERR_LACKING_QUERY_PARAMS = 'Query parameters not provided.'
ERR_PLEASE_PROVIDE = 'Please provide {}.'
ERR_NOT_FOUND = '{} not found'
ERR_NOT_FOUND_WITH_ID = '{} not found with ID: {}'
ERR_ISSUE = 'Issue: {}.'
ERR_NOT_AUTHORIZED = 'You have no authority to perform this action'

########### Authentication Module #################

#REGISTRATION
ERR_BANNED_EMAIL = "This email is banned."
ERR_NO_POLICY_STATUS = "PLease accept or decline the policy."
ERR_NO_POLICY_ACCEPTED = "You need to accept the policy."
ERR_REGISTRATION_FAILED = "Registration failed."
ERR_NO_PASSWORD = "Please provide a password."
ERR_NO_CONFIRMED_PASSWORD = "Please provide a confirmed password."
ERR_NO_NAME = "Please provide a display name."
ERR_WRONG_CONFIMED_PASSWORD = "The confirmed password is not correct."
ERR_INVALID_INPUT_PASSWORD = "The password must have at least 8 characters, at least 1 uppercase, 1 number and 1 special character."
ERR_INVALID_INPUT_NAME = "The display name must be alphanumeric or -, ., _"
ERR_NAME_ALREADY_EXISTED = "The display name {} has already existed."
ERR_NO_MAIL = "Please provide an Email."
ERR_MAIL_INVALID = "The input Email is invalid."
ERR_EMAIL_EXISTED = "The Email {} has already existed, please log in."
ERR_NAME_ALREADY_EXISTED = "The account with the name {} has already existed."
ERR_ACTIVATION_CODE_FAILED_TO_SEND = "Activation code failed to send."
ERR_ACCOUNT_NOT_REGISTERED = "Your account is not registered yet."
ERR_ACTIVATION_CODE_INCORRECT = "The activation code is incorrect or expired. Please go to hoovada.com to request for new code."
ERR_ACC_NOT_REGISTERED = "The account has not been registered."
MSG_ACTIVATION_CODE_SENT = "Activation code has been sent. Please check your Email."
MSG_ACC_ALREADY_ACTIVATED = "Your account has been activated. Please log in."

# PHONE
ERR_NO_PHONE = "Please provide a phone number."
ERR_PHONE_INCORRECT = "The phone number format is incorrect."
ERR_PHONE_ALREADY_EXISTED = "The phone number has already existed. Please log in."
ERR_PHONE_NOT_REGISTERER = "The phone number {} is not registered. Please register."
ERR_PHONE_ACTIVATION_CODE_INCORRECT = "Activation code is incorrect or expired."
ERR_PHONE_NO_CODE = "Please provide phone code."
ERR_PHONE_ACTIVATION_FAILED_TO_SEND = "Activation message failed to send."
MSG_PHONE_ACTIVATION_CODE_SENT = "Activation code has been sent to the phone number {}. Please check the message."

# LOGIN PHONE
ERR_PHONE_NOT_CONFIRMED = "Account related to this phone number is not confirmed. Please check the message to confirm the account."
ERR_PHONE_OR_PASS_INCORRECT = "The phone number or the password is incorrect. "
ERR_PHONE_CODE_INCORRECT = "Login code is incorrect or expired."

# LOGIN - COMMON
ERR_FAILED_LOGIN = "Failed to login."
MSG_LOGOUT_SUCESS = "Successfully logged out."

# RESET PASSWORD
ERR_RESET_CODE_FAILED_TO_SENT = "Reset code failed to send."
ERR_RESET_PASS_INCORRECT = "Reset password code is incorrect or expired. Please go to hoovada.com to request for new reset code."
MSG_RESET_CODE_SENT = "Reset code has been sent. Please check your Email."
MSG_RESET_PASS_SUCCESS = "Password reset successfully. PLease input a new password."
MSG_OTP_SENT = "OTP has been sent."

ERR_NO_TOKEN = "PLease provide access token."
ERR_TOKEN_INCORRECT = "Token is incorrect or expired"
