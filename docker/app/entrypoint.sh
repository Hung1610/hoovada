#!/bin/bash

set -e

flask db migrate	
flask db upgrade

gunicorn -c /opt/docker/app/gunicorn_conf.py --chdir /opt "app:create_app()"
