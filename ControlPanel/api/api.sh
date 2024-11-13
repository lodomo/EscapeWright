#!/bin/bash

pipenv run gunicorn --reload -c ./src/gunicorn.conf.py src.app:app
