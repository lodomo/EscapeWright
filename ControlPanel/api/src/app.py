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
from flask_cors import CORS
from src.pi_node import PiNodeController
from src.redis_funcs import RedisKeys, get_unique_id, update_redis_key, get_redis_key
from src.timer import Timer
from src.yaml_reader import open_yaml_as_dict

app = Flask(__name__)
CORS(app)
worker_key = get_unique_id(RedisKeys().API_WORKER_ID)
timer = Timer()  # Timer shared in redis database
config = open_yaml_as_dict("./src/config.yaml")
pi_node_controller = PiNodeController(config["pi_nodes"])
REDIS = redis.Redis(host="localhost", port=6379, db=0)


@app.route("/load", methods=["GET"])
def load():
    """
    Return the load percentage of the room.
    This will be for letting the front end to know it can open up.
    Right now this is just phony data, TODO real loading.
    """
    percentage = get_redis_key(RedisKeys().API_LOAD_PERCENTAGE)
    percentage = int(percentage)
    new_percentage = percentage + 10
    if new_percentage > 100:
        new_percentage = 100
    update_redis_key(RedisKeys().API_LOAD_PERCENTAGE, str(new_percentage))
    return str(percentage)


@app.route("/control_panel_title", methods=["GET"])
def control_panel_title():
    """
    Return the title of the control panel.
    Useful for the front end to know what the control panel is doing.
    """
    title = "Control Panel for " + config["room_info"]["name"]
    return title


@app.route("/room_name", methods=["GET"])
def room_name():
    """
    Return the title of the room.
    Useful for the front end to know what the room is doing.
    """
    temp_config = open_yaml_as_dict("../config.yaml")
    text = temp_config["room_info"]["name"]
    text = text.upper()
    return text


@app.route("/room_status", methods=["GET"])
def room_status():
    """
    Return the status of the room.
    Useful for the front end to know what the room is doing.
    """

    r = redis.Redis(host="localhost", port=6379, db=0)
    return r.get(RedisKeys().API_ROOM_STATUS)


@app.route("/")
def home():
    """
    This should never really be used. It will tell you which worker
    you're talking to, but that's not useful for anything but making
    sure that the program is running on multiple cores like it's supposed
    to.
    """
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
    if not timer.has_started:
        return "READY"

    if timer.is_paused:
        return "PAUSED"

    if timer.is_stopped:
        return "STOPPED"

    return timer.get_time()


@app.route("/toggle", methods=["GET"])
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


@app.route("/reset/", methods=["GET"])
def reset():
    print("SIMULATING RESET SINCE NO PIS ARE CONNECTED")
    # pi_node_controller.reset_all()
    timer.reset()
    update_redis_key(RedisKeys().API_ROOM_STATUS, "Resetting")
    update_redis_key(RedisKeys().API_LOAD_PERCENTAGE, "0")
    return "Room Reset"


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
        status_was = none
        while true:
            if status != status_was:
                try:
                    status_was = status
                    yield f"data: {status}\n\n"
                except generatorexit:
                    break
                except exception as e:
                    yield f"data: error: {str(e)}\n\n"
            else:
                time.sleep(1)

    return response(room_status_js(), mimetype="text/event-stream")


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
