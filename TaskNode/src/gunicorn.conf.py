"""
Gunicorn Configuration file for the Task Servers.
This handles starting all the globals that need to be initialized
"""

# Settings that are used when running gunicorn with the -c flag.
# These variable names are named by gunicorn. Do not change them.
port = "12413"  # The EscapeWright API Port
bind = f"0.0.0.0:{port}"  # Bind to all interfaces on port 12413
workers = 1  # Number of copies of the application to start
threads = 1  # Number of threads per worker
worker_class = "sync"  # Use the sync worker class
timeout = 60  # One minute timeout for requests
keepalive = 2  # Keep connections open for 2 seconds
max_requests = 500  # Free memory after 500 requests
max_requests_jitter = 50  # Random jitter to prevent simultaneous restarts


def on_starting(server):
    initialize()


def on_reload(server):
    initialize()


def initialize():
    print("Todo: Initialize the Task Server")
    print("This might be totally unnecessary")


def startup_message():
    print(f"Workers: {workers}, Threads: {threads}")
    print(f"Worker class: {worker_class}, Timeout: {timeout}")
    print(f"Keepalive: {keepalive} Max requests: {max_requests}")
    print(f"Jitter: {max_requests_jitter}")
