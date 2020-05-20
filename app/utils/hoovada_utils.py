# # -*- coding: utf-8 -*-
#
# """
# File: utils.py
# Purpose: This file contains some useful and essential function utilities.
#
# This is the applications utilities.
# """
# import codecs
# import hashlib
# import re
# import textwrap
# from datetime import time
#
# import arrow
# import asyncio
# import schedule
# import inflect
# import random
# import markdown2
# from flask_restx import ValidationError
# from quart import (
#     url_for, render_template, request,
#     # copy_current_request_context,
#     # copy_current_app_context
# )
# from quart.ctx import copy_current_app_context, copy_current_request_context
# from io import StringIO
# from app import app
# from typing import Any
# from threading import Thread
# from markdown import Markdown
# from flask_mail import Message
# from inflection import parameterize
# from urllib.parse import urljoin, urlparse
# from werkzeug.routing import BaseConverter
# from itsdangerous import URLSafeTimedSerializer
# from flask_babel import lazy_gettext as _l
# from flask_babel import _
#
# from app.settings import config
# from app.app import mail
# from app.settings import config
#
#
# def random_n_digits(n):
#     range_start = 10 ** (n - 1)
#     range_end = (10 ** n) - 1
#     return random.randint(range_start, range_end)
#
#
# def random_char_slugger():
#     binders = ['-', '.', '_']
#     return random.choice(binders)
#
#
# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return test_url.scheme == 'https' and ref_url.netloc == test_url.netloc
#
#
# async def get_redirect_target():
#     for target in request.args.get('next'), request.referrer:
#         if not target:
#             continue
#         if is_safe_url(target):
#             return target
#
#
# # def send_async_email(app, msg):
# #     with app.app_context():
# #         mail.send(msg)
#
# # async def send_async_email(app, msg):
# #     async with app.app_context():
# #         mail.send(msg)
#
#
# # def send_async_email(app, msg):
# #     result = asyncio.get_event_loop().run_until_complete(_send_async_email(app, msg))
#
# def send_email(
#         subject: str,
#         sender: str,
#         recipients: str,
#         text_body: str,
#         html_body: str,
#         reply_to: str = config.Config.MAIL_DEFAULT_SENDER
# ):
#     msg = Message(subject, sender=sender, reply_to=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)
#     # Thread(target=send_async_email, args=(app, msg)).start()
#
#
# #
# # def send_email(subject, sender, recipients, text_body, html_body, reply_to=app.config['MAIL_DEFAULT_REPLY_TO']):
# #     msg = Message(subject, sender=sender, reply_to=sender, recipients=recipients)
# #     msg.body = text_body
# #     msg.html = html_body
# #     Thread(target=send_async_email, args=(app, msg)).start()
# async def weekly_job():
#     print('WEEKLY_JOB:')
#
#
# # @copy_current_request_context
# # @copy_current_app_context
# async def send_weekly_email():
#     # method = request.method
#     schedule.every(10).seconds.do(weekly_job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
# async def daily_job():
#     print('DAILY_JOB:')
#
#
# # @copy_current_request_context
# # @copy_current_app_context
# async def send_daily_email():
#     schedule.every(5).seconds.do(daily_job)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
# def generate_confirmation_token(email):
#     serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
#     return serializer.dumps(email, salt=config['SECURITY_PASSWORD_SALT'])
#
#
# def confirm_token(token, expiration=3600):
#     serializer = URLSafeTimedSerializer(config['SECRET_KEY'])
#     try:
#         email = serializer.loads(
#             token,
#             salt=config['SECURITY_PASSWORD_SALT'],
#             max_age=expiration
#         )
#         return email
#     except:
#         return False
#
#
# # def generate_url(id):
# #     hashed_id = hashlib.pbkdf2_hmac(
# #         'sha512',
# #         codecs.encode(id, 'utf-8'),
# #         codecs.encode(salt, 'utf-8'),
# #         10000
# #     )
# #     hostname = request.host
# #     route = url_for('validate_user', id=hashed_id, _external=True, _scheme='https'),
# #
# #     return "https://" + hostname + route
#
#
# def flash_errors(errors, flash):
#     for field in errors:
#         for error in errors[field]:
#             flash(error)
#
#
# def password_validator(form, field):
#     """Ensure that passwords have at least 6 characters with one lowercase letter, one uppercase letter and one number.
#
#     Override this method to customize the password validator.
#     """
#
#     # Convert string to list of characters
#     password = list(field.data)
#     password_length = len(password)
#
#     # Count lowercase, uppercase and numbers
#     lowers = uppers = digits = 0
#     for ch in password:
#         if ch.islower():
#             lowers += 1
#         if ch.isupper():
#             uppers += 1
#         if ch.isdigit():
#             digits += 1
#
#     # Password must have one lowercase letter, one uppercase letter and one digit
#     is_valid = password_length >= 6 and lowers and uppers and digits
#     if not is_valid:
#         raise ValidationError(_l(
#             'Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))
#
#
# # If you prefer using Regex:
# # from re import compile
# # PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z')
# # def password_is_valid(password):
# #     return PASSWORD_REGEX.match(password) is not None
#
# def username_validator(form, field):
#     """Ensure that Usernames contains at least 5 alphanumeric characters.
#     """
#     username = field.data
#     if len(username) < 5:
#         raise ValidationError(_l('Username must be at least 5 characters long'))
#     valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._'
#     chars = list(username)
#     for char in chars:
#         if char not in valid_chars:
#             raise ValidationError(_l("Username may only contain letters, numbers, '-', '.' and '_'"))
#
#     # If you prefer using Regex:
#     # from re import compile
#     # USERNAME_REGEX = compile(r'\A[\w\-\.]{3,}\Z')
#     # def username_is_valid(username):
#     #     return USERNAME_REGEX.match(username) is not None
#
#
# def unmark_element(element, stream=None):
#     if stream is None:
#         stream = StringIO()
#     if element.text:
#         stream.write(element.text)
#     for sub in element:
#         unmark_element(sub, stream)
#     if element.tail:
#         stream.write(element.tail)
#     return stream.getvalue()
#
#
# # patching Markdown
# Markdown.output_formats["plain"] = unmark_element
# __md = Markdown(output_format="plain")
# __md.stripTopLevelTags = False
#
#
# def convert_markdown(string):
#     """Convert the argument from markdown to html"""
#     return markdown2.markdown(string,
#                               extras=["code-friendly", "code-color", "footnotes"])
#
#
# def remove_markdown(text):
#     return __md.convert(text)
#
#
# def normalize(string):
#     """Unify string"""
#     string = re.sub(r"[^\w]+", " ", string)
#     string = "-".join(string.lower().strip().split())
#     return string
#
#
# def normalize_topics(string):
#     """Return a list of normalized topics from a string with comma separated
#     topics"""
#     topics = string.split(',')
#     result = []
#     for topic in topics:
#         normalized = normalize(topic)
#         if normalized and not normalized in result:
#             result.append(normalized)
#     return result
#
#
# # def tidy_topics(question):
# #     """Remove topics with zero associations"""
# #     for topic in Topic.query.filter_by(questions=None):
# #         db.session.delete(topic)
# #     db.session.commit()
#
# def make_headers(response):
#     # response.headers['accept-encoding'] = 'gzip, deflate, br'
#     # response.headers['Service-Worker-Allowed'] = '/'
#     # response.headers['Pragma'] = 'public'
#     # response.headers['Cache-Control'] = 'public'
#     # response.headers['Vary'] = 'Accept-Encoding'
#     # response.headers['cache-control'] = 'max-age=2592000'
#     response.headers['Access-Control-Allow-Origin'] = '*';
#     # response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#     # response.headers['Access-Control-Allow-Headers'] = 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range'
#     # response.headers['Access-Control-Max-Age'] = 1728000
#     # response.headers['Content-Type'] = 'text/plain; charset=utf-8'
#     # response.headers['Content-Length'] = 0
#     return response
#
#
# # async def make_promises(response):
# #     await make_push_promise(url_for('static', filename='css/picnic.min.css', _external=True, _scheme='https'))
# # #    response.push_promises.add(url_for('static', filename='css/picnic.min.css', _external=True, _scheme='https'))
# #     response.push_promises.add(url_for('static', filename='css/style.css', _external=True, _scheme='https'))
# #     return response
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['PRO_PIC_ALLOWED_EXTENSIONS']
#
#
# class URLSlugConverter(BaseConverter):
#     '''Matches an id with optional slug'''
#
#     regex = r'-?\d+(?:/[\w\-]*)?'
#
#     def __init__(self, attr='title', length=80):
#         self.attr = attr
#         self.length = int(length)
#         # super(IDSlugConverter, self).__init__(map)
#
#     def to_python(self, value):
#         id, slug = (value.split('/') + [None])[:2]
#         return int(id)
#
#     def to_url(self, value):
#         raw = str(value) if self.attr is None else getattr(value, self.attr, '')
#         slug = parameterize(raw)[:self.length].rstrip('-')
#         return f'{value.id}/{slug}'.rstrip('/')
#
#
# class UserURLSlugConverter(BaseConverter):
#     '''Matches an id with optional slug'''
#
#     regex = r'-?[\w\-]*-\d+()?'
#
#     def __init__(self, attr='display_name', length=80):
#         self.attr = attr
#         self.length = int(length)
#         # super(IDSlugConverter, self).__init__(map)
#
#     def to_python(self, value):
#         print(f'to_python value: {value}')
#         id = int(value.split('-')[-1])
#         print(f'to_python id: {id}')
#         return id
#
#     def to_url(self, value):
#         print(f'to_url value: {value}')
#         raw = str(value) if self.attr is None else getattr(value, self.attr, '')
#         print(f'to_url raw: {raw}')
#         slug = parameterize(raw)[:self.length].rstrip('-')
#         print(f'to_url slug: {slug}')
#         url = f'{slug}-{value.id}'.rstrip('/')
#         print(f'to_url url: {url}')
#         return url
#
#
# def to_upper(value):
#     return value.upper()
#
#
# def plural(count, word):
#     p = inflect.engine()
#     return p.plural(word, count)
#
#
# def title(text):
#     return text.title()
#
#
# def humanize_time(time):
#     ts = arrow.get(time)
#     return ts.humanize()
#
#
# def asked_date(date):
#     ds = arrow.get(date)
#     return f"asked {ds.format('MMM DD YYYY')} at {ds.format('HH:mm')}"
#
#
# def answered_date(date):
#     ds = arrow.get(date)
#     return f"answered {ds.format('MMM DD YYYY')} at {ds.format('HH:mm')}"
#
#
# def nice_date(date):
#     ds = arrow.get(date)
#     return f"{ds.format('MMM DD YYYY')} at {ds.format('HH:mm')}"
#
#
# def short_nice_date(date):
#     ds = arrow.get(date)
#     return f"{ds.format('ddd')} at {ds.format('HH:mm')}"
#
#
# def ellipsis(text, length=200):
#     return textwrap.shorten(text, width=length, placeholder="...")
#
#
# def string_it(text):
#     return str(text)
