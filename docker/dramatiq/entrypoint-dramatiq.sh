#!/bin/bash

set -e

cd /opt; dramatiq dramatiq_queue:rabbitmq_broker
