#!/bin/bash

# Default host to make it available to all devices in the network
HOST=0.0.0.0

# 12413 is the default API port for EscapeWright
PORT=12413

# Run the app inside the virtual environment
# gunicorn is a WSGI HTTP server for Python web applications
# --worker-class gevent is a coroutine-based Python networking library.
# --workers 1 is the number of worker processes for handling requests. In the extreme case of 30 clients, 1 worker is enough.
# --threads 4 is the number of threads per worker process. The default is 1, but we can increase it to 4 to help with I/O-bound tasks.
# --bind $HOST:$PORT is the address and port to bind the server to.
# app:app is the module and application name to run.
pipenv run gunicorn --worker-class gevent --workers 1 --threads 4 --bind $HOST:$PORT app:app
