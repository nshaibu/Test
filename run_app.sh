#!/bin/bash

set -o errexit

python manage.py migrate
python manage.py runserver 0.0.0.0:8070