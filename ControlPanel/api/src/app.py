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
from flask import Flask, jsonify
from flask_cors import CORS
import markdown
from src.pi_node import PiNodeController
from src.redis_keys import RedisKeys
from src.timer import Timer  # Treated as a global Timer()
from src.yaml_reader import open_yaml_as_dict

app = Flask(__name__)
CORS(app)
config = open_yaml_as_dict(RedisKeys().API_YAML_CONFIG_DATA())
worker_key = RedisKeys().get_unique_id(RedisKeys().API_WORKER_ID)
pi_node_controller = PiNodeController(config["pi_nodes"])


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


def room_name():
    """
    Return the title of the room.
    Useful for the front end to know what the room is doing.
    """
    temp_config = open_yaml_as_dict(RedisKeys().API_YAML_CONFIG_DATA())
    text = temp_config["room_info"]["name"]
    text = text.upper()
    return text


@app.route("/")
def home():
    """
    This should be a mini api interface just to make
    sure everything works.
    """
    html = "<p>API Interface</p>"
    html += f"<p>Worker Key: {worker_key}</p>"
    html += "<p>End points</p>"
    return html, 200


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


@app.route("/toggle", methods=["POST"])
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


@app.route("/reset", methods=["POST"])
def reset():
    print("SIMULATING RESET SINCE NO PIS ARE CONNECTED")
    # pi_node_controller.reset_all()
    Timer().reset()
    RedisKeys().update_key(RedisKeys().API_ROOM_STATUS, "LOADING")
    RedisKeys().update_key(RedisKeys().API_LOAD_PERCENTAGE, "0")
    return "Room Reset"

@app.route("/stop", methods=["POST"])
def stop():
    """
    Stop the room.
    """
    Timer().stop()
    broadcast("stop")
    RedisKeys().update_key(RedisKeys().API_ROOM_STATUS, "STOPPED")
    return "Room Stopped", 200


@app.route("/script", methods=["GET"])
def script():
    """
    Return the script for the room.
    This gives the front end the script to display for the gameguide.
    """
    # Open file and return the contents.
    script_file = config["script"]
    script_data = ""
    with open(script_file, "r") as f:
        script_data = f.read()

    html = markdown.markdown(script_data)
    return html


@app.route("/pi_statuses", methods=["GET"])
def pi_statuses():
    """
    Get the statuses of all the pi nodes.
    """
    pi_dicts = pi_node_controller.get_serializable_pis()
    return jsonify(pi_dicts)


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


if __name__ == "__main__":
    app.run()
