#!/bin/bash

# Workers is 2x the number of cores + 1. Raspberry Pi 4 has 4 cores.
WORKERS=9

# Threads isn't precise, this is purely an experimental guess
THREADS=4

HOST=0.0.0.0
PORT=12413

pipenv run gunicorn --workers $WORKERS --threads $THREADS --bind $HOST:$PORT app:app
