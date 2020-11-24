#!/bin/bash

set -e

flask db migrate	
flask db upgrade

(gunicorn -c docker/app/gunicorn_conf.py "app:flask_app") & (dramatiq dramatiq_queue:rabbitmq_broker)
