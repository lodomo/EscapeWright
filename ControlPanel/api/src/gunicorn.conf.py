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
    RedisKeys().init_keys()
    Timer(new_timer=True)
    create_pis()
    print(f"Workers: {workers}, Threads: {threads}")
    print(f"Worker class: {worker_class}, Timeout: {timeout}")
    print(f"Keepalive: {keepalive} Max requests: {max_requests}")
    print(f"Jitter: {max_requests_jitter}")


def create_pis():
    config = open_yaml_as_dict(RedisKeys().API_YAML_CONFIG_DATA())
    pi_node_controller = PiNodeController(config["pi_nodes"], initial=True)
    pi_node_controller.clear_all_statuses()
    pi_node_controller.print_all()
