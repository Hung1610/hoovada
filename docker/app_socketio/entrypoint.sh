#!/bin/bash

set -e

gunicorn -c /opt/docker/app_socketio/gunicorn_conf.py --chdir /opt "app_socketio:create_app()"
