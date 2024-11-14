# gunicorn.conf.py
from src.pi_node import PiNodeController
from src.redis_keys import RedisKeys
from src.yaml_reader import open_yaml_as_dict
from src.timer import Timer

port = "12413"  # The EscapeWright port
bind = f"0.0.0.0:{port}"  # Bind to all interfaces on port 12413
workers = 5  # Number of copies of the application to start
threads = 2  # Number of threads per worker
worker_class = "gthread"  # Threaded worker class
timeout = 60  # One minute timeout for requests
keepalive = 2  # Keep connections open for 2 seconds
max_requests = 500  # Free memory after 500 requests
max_requests_jitter = 50  # Random jitter to prevent simultaneous restarts


def on_starting(server):
    print("Starting server...")
    initialize_pid()
    RedisKeys.API_WORKER_ID.set(0)
    RedisKeys.API_ROOM_STATUS.set("LOADING")
    RedisKeys.API_LOAD_PERCENTAGE.set(0)
    RedisKeys.API_YAML_CONFIG.set("./src/config.yaml")
    Timer(new_timer=True)
    create_pis()
    print(f"Workers: {workers}, Threads: {threads}")
    print(f"Worker class: {worker_class}, Timeout: {timeout}")
    print(f"Keepalive: {keepalive} Max requests: {max_requests}")
    print(f"Jitter: {max_requests_jitter}")


def initialize_pid():
    """
    Initialize the PID for the gunicorn server.
    This file is set from the gunicorn command line.
    --pid ./src/gunicorn.pid
    """
    try:
        file_name = "./src/gunicorn.pid"
        with open(file_name, "r") as file:
            gunicorn_id = file.read()
        print(f"Gunicorn PID: {gunicorn_id}")
        RedisKeys.GUNICORN_PID.set(gunicorn_id)
    except FileNotFoundError:
        print("No PID file found. Rerun the server with the --pid flag.")


def create_pis():
    config = open_yaml_as_dict(RedisKeys.API_YAML_CONFIG.get())
    pi_node_controller = PiNodeController(config["pi_nodes"], initial=True)
    pi_node_controller.clear_all_statuses()
    pi_node_controller.print_all()
