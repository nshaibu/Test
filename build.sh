#!/bin/bash

export USER_ID=$(id -u)
export GID=$(id -g)

docker-compose build
docker-compose up
