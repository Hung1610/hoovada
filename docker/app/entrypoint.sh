#!/bin/bash

set -e

flask db upgrade

exec gunicorn -c docker/app/gunicorn_conf.py --preload "app.manage:flask_app"
