# gunicorn.conf.py
import redis
from src.timer import Timer
from src.pi_node import PiNodeGenerator, PiNodeController, PiNode

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
    set_redis_workers()
    create_timer()
    create_pis()
    print(f"Workers: {workers}, Threads: {threads}")
    print(f"Worker class: {worker_class}, Timeout: {timeout}")
    print(f"Keepalive: {keepalive} Max requests: {max_requests}")
    print(f"Jitter: {max_requests_jitter}")


def set_redis_workers():
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.set("APIWorkerID", 0)
        print("APIWorkerID set to 0 in Redis")
    except Exception as e:
        print(f"Error setting APIWorkerID in Redis: {e}")
        exit(1)


def create_timer():
    try:
        timer = Timer()
        timer.save_to_redis()
        print("New Timer created and saved to Redis")
    except Exception as e:
        print(f"Error setting Timer in Redis: {e}")
        exit(1)


def create_pis():
    pi_list = "./src/pi_list.ew"
    pi_node_generator = PiNodeGenerator(pi_list)
    pi_node_controller = PiNodeController(pi_node_generator.generate())
    pi_node_controller.clear_all_statuses()
    pi_node_controller.print_all()
