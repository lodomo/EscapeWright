#!/bin/bash

pipenv run gunicorn -c ./src/gunicorn.conf.py src.app:app
