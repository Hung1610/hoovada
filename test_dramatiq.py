from os import environ

RABBITMQ_PORT = environ.get('RABBITMQ_PORT', '32520')
RABBITMQ_HOST = environ.get('RABBITMQ_HOST', '128.199.80.171')
RABBITMQ_USER = environ.get('RABBITMQ_USER', 'thPntnLV-00oipgB6VtzN4Cb_CVT4kUL')
RABBITMQ_PASSWORD = environ.get('RABBITMQ_USER', '-3x9QHlVJEPjJdPqnGqLzh0clCkRKI12')
RABBITMQ_URL = 'amqp://' \
    + RABBITMQ_USER + ':' + RABBITMQ_PASSWORD + '@' + RABBITMQ_HOST + ':' + RABBITMQ_PORT

print(RABBITMQ_URL)

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)
import requests
import sys


@dramatiq.actor
def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(" "))
    print(f"There are {count} words at {url!r}.")


if __name__ == "__main__":
    count_words.send(sys.argv[1])