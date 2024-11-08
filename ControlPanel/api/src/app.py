#############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Control the A Simulated Reality Experience
#     Version: 0.0.1 - Derived from Code Samurai Version 2.X
# Description: Backend API for communicating with the pi nodes.
#              This should not be ran directly, instead through a gunicorn
#              server.
#
###############################################################################

import redis
from flask import Flask

app = Flask(__name__)


def increment_worker_key():
    r = redis.Redis(host='localhost', port=6379, db=0)
    redis_key = "APIWorkerID"
    lock = r.lock("worker_lock", timeout=5)

    try:
        if lock.acquire(blocking=True):
            if not r.exists(redis_key):
                r.set(redis_key, 0)
            cur = r.get(redis_key)
            r.incr(redis_key)
            return int(cur)
        else:
            print("Could not acquire lock.")
            exit(1)
    finally:
        # Release the lock
        lock.release()


worker_key = increment_worker_key()
print(f"I am worker {worker_key}")


@app.route("/")
def home():
    return f"You're talking to worker {worker_key}"


"""
OLD GARBAGE

# Create the a controller for all the pi nodes.
pi_list_file = "pi_list.ew"
pi_list = PiNodeGenerator(pi_list_file).generate()
pi_node_controller = PiNodeController(pi_list)
pi_node_controller.print_all()
room_timer = Timer()
status = "idle"

# from src.pi_node import PiNode
from src.pi_node_controller import PiNodeController
from src.pi_node_generator import PiNodeGenerator
from src.timer import Timer

@app.route("/")
def home():
    return "There is no reason to be here."


@app.route("/time_remaining", methods=["GET"])
def time_remaining():
    def time_remaining_js():
        while True:
            try:
                time.sleep(1)
                yield f"data: {room_timer.get_time()}\n\n"
            except GeneratorExit:
                break
            except Exception as e:
                yield f"data: ERROR: {str(e)}\n\n"

    return Response(time_remaining_js(), mimetype="text/event-stream")


@app.route("/room_status", methods=["GET"])
def room_status():
    def room_status_js():
        status_was = None
        while True:
            if status != status_was:
                try:
                    status_was = status
                    yield f"data: {status}\n\n"
                except GeneratorExit:
                    break
                except Exception as e:
                    yield f"data: ERROR: {str(e)}\n\n"
            else:
                time.sleep(1)

    return Response(room_status_js(), mimetype="text/event-stream")


@app.route("/toggle", methods=["POST"])
def toggle():
    global status

    # if the room is not running, start it.
    if room_timer.__start_time is None:
        room_timer.start()
        status = "RUNNING"
        logging.info("Starting room")
        broadcast("room_start")
        return "Room Started"

    # if the room is running, pause it.
    if not room_timer.__is_paused:
        room_timer.pause()
        status = "PAUSED"
        logging.info("Pausing room")
        broadcast("pause")
        return "Room Paused"

    # else, resume it.
    room_timer.resume()
    status = "RUNNING"
    logging.info("Resuming room")
    broadcast("resume")
    return "Room Resumed"


@app.route("/start/", defaults={"gameguide": "None", "players": "None"})
@app.route("/start/<gameguide>/<players>", methods=["POST"])
def start(gameguide, players):
    # Start the room
    # Get confirmation from the user, then start the room
    # This will likely require a hard reboot
    toggle()
    logging.info("ROOM START")
    logging.info("GAME GUIDE: " + gameguide)
    logging.info("PLAYERS: " + players)
    return "Room Started", 200


@app.route("/reset", methods=["POST"])
def reset():
    status = "RESETTING"
    pi_node_controller.reset_all()
    room_timer.reset()
    logging.info("Resetting all nodes")

@app.route("/trigger/<message>", methods=["POST"])
def trigger(self, message):
        self.client_controller.broadcast(message)
        return
"""


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, threaded=True)
