#!/bin/bash

set -e

flask db migrate	
flask db upgrade

#gunicorn --log-config ./gunicorn_logging.conf --worker-tmp-dir /dev/shm  --worker-connections 1001 --workers 4 --threads=4 --worker-class=gthread -b 0.0.0.0:5000 wsgi:app
gunicorn --worker-tmp-dir /dev/shm  --worker-connections 1001 --workers 4 --threads=4 --worker-class=gthread -b 0.0.0.0:5000 wsgi:app
