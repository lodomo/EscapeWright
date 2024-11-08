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

from flask import Flask
from src.redis_funcs import get_unique_id
from src.timer import Timer
from src.pi_node import PiNodeGenerator, PiNodeController

app = Flask(__name__)
worker_key = get_unique_id("APIWorkerID")
timer = Timer()  # Timer shared in redis database

pi_list_file = "./src/pi_list.ew"
pi_node_generator = PiNodeGenerator(pi_list_file)
pi_node_controller = PiNodeController(pi_node_generator.generate())


@app.route("/")
def home():
    return f"Worker {worker_key}, reporting for duty!"


@app.route("/start/", defaults={"gameguide": "None", "players": "None"})
@app.route("/start/<gameguide>/<players>", methods=["POST"])
def start(gameguide, players):
    """
    Start the room!
    Get the gameguide name and number of players
    This will eventually log the room running in a database
    """
    toggle()
    return "Room Started", 200


@app.route("/time_remaining", methods=["GET"])
def time_remaining():
    return timer.get_time()


@app.route("/toggle", methods=["POST"])
def toggle():

    if not timer.has_started:
        timer.start()
        broadcast("room_start")
        return "Room Started"

    if not timer.is_paused:
        timer.pause()
        broadcast("pause")
        return "Room Paused"

    timer.resume()
    broadcast("resume")
    return "Room Resumed"


@app.route("/trigger/<message>", methods=["POST"])
def trigger(self, message):
    broadcast(message)
    return


def broadcast(message: str):
    """
    TODO
    """
    print("TODO")
    return


def get_pi_statuses():
    """
    Get the statuses of all the pi nodes.
    """
    print("TODO")
    return


def aggressively_get_pi_statuses():
    """
    Get the statuses of all the pi nodes.
    Do not stop until all the statuses are received as Ready.
    """
    print("TODO")
    return


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
