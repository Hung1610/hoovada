#!/bin/bash

set -e

#if [[ -d /migrations ]]; then
#    echo "Removing migrations folders"
#    rm -rf /migrations
#fi

#flask db init
#flask db stamp head
#flask db migrate

flask db migrate	
flask db stamp head

gunicorn --worker-tmp-dir /dev/shm  --worker-connections 1001 --workers 4 --threads=4 --worker-class=gthread -b 0.0.0.0:5000 wsgi:app
