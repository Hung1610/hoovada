#!/bin/bash

set -e

flask db migrate	
flask db upgrade

cd /opt; dramatiq app:broker -p 1
