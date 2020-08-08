#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class AuthDto(Dto):
    name = 'auth'
    api = Namespace(name, description='auth related operations')

    model_sms_register = api.model('sms_register', {
        'display_name': fields.String(required=False),
        'phone_number': fields.String(required=True),
        'password': fields.String(required=True)
    })
    
    model_confirm_sms = api.model('confirm_sms', {
        'phone_number': fields.String(required=True),
        'code': fields.String(required=True)
    })
    
    model_resend_confirmation_sms = api.model('resend_confirmation_sms', {
        'phone_number': fields.String(required=True),
    })
    
    model_sms_login_with_password = api.model('sms_login_with_password', {
        'phone_number': fields.String(required=True),
        'password': fields.String(required=True),
    })
    
    model_sms_login_with_code = api.model('sms_login_with_code', {
        'phone_number': fields.String(required=True),
    })
    
    model_sms_login_with_code_confirm = api.model('sms_login_with_code_confirm', {
        'phone_number': fields.String(required=True),
        'code': fields.String(required=True),
    })

    model_register = api.model('register', {
        'display_name': fields.String(required=False),
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })

    model_login = api.model('login', {
        'email': fields.String(required=True),
        'password': fields.String(requried=True)
    })

    model_social_login = api.model('social_login', {
        'access_token': fields.String(required=True),
    })

    model_reset_password_email = api.model('reset_password_email', {
        'email': fields.String(required=True),
    })

    model_reset_password_phone = api.model('reset_password_phone', {
        'phone_number': fields.String(required=True),
    })

    model_change_password_token = api.model('change_password_token', {
        'reset_token': fields.String(required=True),
        'token_type': fields.String(required=True, choices=('email', 'phone')),
        'password': fields.String(required=True),
        'password_confirm': fields.String(required=True),
    })

    model_change_password = api.model('change_password', {
        'old_password': fields.String(required=True),
        'password': fields.String(required=True),
        'password_confirm': fields.String(required=True),
    })

    message_response = api.model('response', {
        'message': fields.String(required=True)
    })