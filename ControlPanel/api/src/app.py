#############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Control the A Simulated Reality Experience
#     Version: 0.0.1 - Derived from Code Samurai Version 2.X, Vastly Different
# Description: Backend API for communicating with the pi nodes.
#              This should not be ran directly, instead through a gunicorn
#              server.
#
###############################################################################

import redis
from flask import Flask
from flask_cors import CORS
from src.pi_node import PiNodeController
from src.redis_keys import RedisKeys
from src.timer import Timer  # Treated as a global Timer()
from src.yaml_reader import open_yaml_as_dict

app = Flask(__name__)
CORS(app)
worker_key = RedisKeys().get_unique_id(RedisKeys().API_WORKER_ID)
config = open_yaml_as_dict(RedisKeys().API_YAML_CONFIG_DATA())
pi_node_controller = PiNodeController(config["pi_nodes"])
REDIS = redis.Redis(host="localhost", port=6379, db=0)


@app.route("/status", methods=["GET"])
def status():
    """
    Return the status of the room.
    Useful for the front end to know what the room is doing.
    """
    if RedisKeys().API_ROOM_STATUS_DATA() == "LOADING":
        load()

    return RedisKeys().API_ROOM_STATUS_DATA(), 200


def load() -> int:
    """
    Return the load percentage of the room.
    This will be for letting the front end to know it can open up.
    Right now this is just phony data, TODO real loading.
    """
    percent = RedisKeys().API_LOAD_PERCENTAGE_DATA()
    percent = int(percent)
    new_percent = percent + 10
    if new_percent > 100:
        new_percent = 100
    RedisKeys().update_key(RedisKeys().API_LOAD_PERCENTAGE, str(new_percent))
    if new_percent == 100:
        RedisKeys().update_key(RedisKeys().API_ROOM_STATUS, "READY")
    return new_percent


@app.route("/control_panel_title", methods=["GET"])
def control_panel_title():
    """
    Return the title of the control panel.
    Useful for the front end to know what the control panel is doing.
    """
    title = "Control Panel for " + config["room_info"]["name"]
    return title, 200


@app.route("/room_name", methods=["GET"])
def room_name():
    """
    Return the title of the room.
    Useful for the front end to know what the room is doing.
    """
    temp_config = open_yaml_as_dict(RedisKeys().API_YAML_CONFIG_DATA())
    text = temp_config["room_info"]["name"]
    text = text.upper()
    return text, 200


@app.route("/")
def home():
    """
    Currently this shows just the worker ID.
    In the future it should be a mini front end where I can type
    in commands that I want to do.
    """
    return f"Worker {worker_key}, reporting for duty!", 200


@app.route("/start/", defaults={"gameguide": "None", "players": "None"})
@app.route("/start/<gameguide>/<players>", methods=["POST"])
def start(gameguide, players):
    """
    Start the room!
    Get the gameguide name and number of players
    This will eventually log the room running in a database
    """
    if Timer().has_started:
        return "Error: Room Already Started", 400

    toggle()
    return "Room Started", 200


@app.route("/time_remaining", methods=["GET"])
def time_remaining():
    if Timer().has_started:
        return Timer().get_time(), 200

    return status()


@app.route("/toggle", methods=["GET"])
def toggle():
    timer = Timer()
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


@app.route("/trigger/", defaults={"message": "None"})
@app.route("/trigger/<message>", methods=["POST"])
def trigger(message):
    broadcast(message)
    return "Not Implemented", 501


@app.route("/relay/", defaults={"message": "None", "pi_node": "None"})
@app.route("/relay/<message>/<pi_node>", methods=["POST"])
def relay(message, pi_node):
    """
    TODO
    """
    return "Not Implemented", 501


@app.route("/reset/", methods=["GET"])
def reset():
    print("SIMULATING RESET SINCE NO PIS ARE CONNECTED")
    # pi_node_controller.reset_all()
    Timer().reset()
    RedisKeys().update_key(RedisKeys().API_ROOM_STATUS, "LOADING")
    RedisKeys().update_key(RedisKeys().API_LOAD_PERCENTAGE, "0")
    return "Room Reset"


@app.route("/script", methods=["GET"])
def script():
    """
    Return the script for the room.
    This gives the front end the script to display for the gameguide.
    """
    # Open file and return the contents.
    filename = config["script"]
    with open(filename, "r") as file:
        text = ""
        for line in file:
            text += line
            text += "\n"
    return text, 200


def broadcast(message: str):
    """
    TODO
    """
    print("TODO BROADCAST")
    return


def get_pi_statuses():
    """
    Get the statuses of all the pi nodes.
    """
    print("TODO GET PI STATUSES")
    return


def aggressively_get_pi_statuses():
    """
    Get the statuses of all the pi nodes.
    Do not stop until all the statuses are received as Ready.
    """
    print("TODO AGGRESSIVELY GET PI STATUSES")
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
    app.run()
