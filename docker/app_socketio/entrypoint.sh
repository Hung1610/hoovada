#!/bin/bash

set -e

exec gunicorn -c docker/app_socketio/gunicorn_conf.py "app_socketio:create_app()"
