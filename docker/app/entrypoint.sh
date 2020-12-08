#!/bin/bash

set -e

flask db migrate	
flask db upgrade

gunicorn -c docker/app/gunicorn_conf.py "app.manage:flask_app"
