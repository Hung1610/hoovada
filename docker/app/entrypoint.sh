#!/bin/bash

set -e

flask db downgrade 8ddcb63384d6

flask db upgrade

exec gunicorn -c docker/app/gunicorn_conf.py "app.manage:flask_app"
