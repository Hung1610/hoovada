#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from os import environ

# third-party modules
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.message import Message

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

def test():
    rabbitmq_broker.enqueue(Message(queue_name='app_queue', actor_name='test', args=(), kwargs={}, options={}))


def push_notif_to_specific_users_produce(message, user_ids):
    rabbitmq_broker.enqueue(Message(queue_name='app_notif_queue', \
        actor_name='push_notif_to_specific_users', \
        args=(), \
        kwargs={'message': message, 'user_ids': user_ids}, \
        options={}))

def push_basic_notification_produce(message):
    rabbitmq_broker.enqueue(Message(queue_name='app_notif_queue', \
        actor_name='push_basic_notification', \
        args=(), \
        kwargs={'message': message}, \
        options={}))

@dramatiq.actor()
def send_weekly_registered_users():
    pass

@dramatiq.actor()
def update_seen_poll(user_id, poll_id):
    pass

@dramatiq.actor()
def update_seen_questions(question_id, user_id):
    pass
    

@dramatiq.actor()
def update_seen_articles(article_id, user_id):
    pass

@dramatiq.actor()
def update_reputation(topic_id, voter_id, is_voter=False):
    pass

@dramatiq.actor()
def send_weekly_recommendation_mails():
    pass

@dramatiq.actor()
def send_daily_recommendation_mails():
    pass

@dramatiq.actor()
def send_daily_similar_mails():
    pass

@dramatiq.actor()
def send_weekly_similar_mails():
    pass

@dramatiq.actor()
def send_recommendation_mail(user_id):
    pass

@dramatiq.actor()
def send_similar_mail(user_id):
    pass

@dramatiq.actor()
def send_daily_new_topics():
    pass

@dramatiq.actor()
def send_weekly_new_topics():
    pass

@dramatiq.actor()
def send_new_topics(user_id):
    pass

#@dramatiq.actor()
#def new_article_notify_user_list(article_id, user_ids):
#    pass

#@dramatiq.actor()
#def new_question_notify_user_list(question_id, user_ids):
#    pass

#@dramatiq.actor()
#def new_answer_notify_user_list(answer_id, user_ids):
#    pass