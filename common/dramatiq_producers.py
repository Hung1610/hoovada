#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from os import environ

# third-party modules
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from flask import current_app, g

# own modules


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


RABBITMQ_PORT = environ.get('RABBITMQ_PORT', '32520')
RABBITMQ_HOST = environ.get('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_USER = environ.get('RABBITMQ_USER', '')
RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD', '')
RABBITMQ_URL = 'amqp://' + RABBITMQ_USER + ':' + RABBITMQ_PASSWORD + '@' +\
    environ.get('RABBITMQ_URL',  RABBITMQ_HOST + ':' + RABBITMQ_PORT)
rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)


# Define dramatiq actor here.
# Call these methods from common. tasks.py in each app will act as listenner for events (aka consumer).

@dramatiq.actor()
def test():
    pass

@dramatiq.actor()
def update_seen_questions(question_id, user_id):
    pass
    

@dramatiq.actor()
def update_seen_articles(article_id, user_id):
    pass

@dramatiq.actor()
def send_recommendation_mail(user):
    pass

@dramatiq.actor()
def send_similar_mail(user):
    pass