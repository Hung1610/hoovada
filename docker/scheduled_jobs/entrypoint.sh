#!/bin/bash

set -e

exec pypy3 -m scheduled_jobs.manage
