#!/bin/bash

GUNICORN_CONF=./src/gunicorn.conf.py
GUNICORN_PID=./src/gunicorn.pid

pipenv run gunicorn --reload -c $GUNICORN_CONF --pid $GUNICORN_PID src.app:app
