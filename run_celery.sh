#!/bin/bash

set -o errexit

celery -A program_test worker -l info
