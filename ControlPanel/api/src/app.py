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

import os
from flask import Flask, jsonify
from flask_cors import CORS
import markdown
from src.pi_node import PiNodeController
from src.redis_keys import RedisKeys
from src.timer import Timer  # Treated as a global Timer()
from src.yaml_reader import open_yaml_as_dict

app = Flask(__name__)
CORS(app)
config = open_yaml_as_dict(RedisKeys.API_YAML_CONFIG.get())
worker_key = RedisKeys.API_WORKER_ID.get_then_increment()
pi_node_controller = PiNodeController(config["pi_nodes"])


@app.route("/payload", methods=["GET"])
def payload():
    """
    Returns a full data payload for the room.
    This might be good to just call all the time and get the data you want.
    """
    return jsonify(generate_payload()), 200


def generate_payload():
    """
    Returns a full data payload for the room.
    This might be good to just call all the time and get the data you want.
    This little bit of extra processing comes at a freebie for updating anything
    on the fly. Since the data is tiny it's not a big deal to open the config
    file every time.

    If this grows too large, I can have it cache the config instead.
    """
    config = open_yaml_as_dict(RedisKeys.API_YAML_CONFIG.get())

    payload = {}
    payload["room_name"] = config["room_info"]["name"].upper()
    payload["control_panel_title"] = "Control Panel for " + config["room_info"]["name"]
    payload["room_status"] = RedisKeys.API_ROOM_STATUS.get()
    payload["time_remaining"] = Timer().get_time()
    #payload["pi_statuses"] = 
    #payload["script"] = 
    return payload


def get_payload_data(data: str):
    """
    Get the payload data for the room.
    """
    payload = generate_payload()
    return payload[data]


@app.route("/room_name", methods=["GET"])
def room_name():
    """
    Return the title of the room.
    Useful for the front end to know what the room is doing.
    """
    return get_payload_data("room_name"), 200


@app.route("/control_panel_title", methods=["GET"])
def control_panel_title():
    """
    Return the title of the control panel.
    Useful for the front end to know what the control panel is doing.
    """
    payload = generate_payload()
    return payload["control_panel_title"], 200


@app.route("/status", methods=["GET"])
def status():
    """
    Return the status of the room.
    Useful for the front end to know what the room is doing.
    """
    return RedisKeys.API_ROOM_STATUS.get(), 200


@app.route("/time_remaining", methods=["GET"])
def time_remaining():
    return get_payload_data("time_remaining"), 200


@app.route("/restart_server", methods=["POST"])
def restart_server():
    """
    Restart the server.
    """
    pid = RedisKeys.GUNICORN_PID.get()
    print(f"Restarting server with PID: {pid}")
    yield "Restarting Server"
    os.system(f"kill -HUP {pid}")
    return "Server Restarted", 200


def load() -> int:
    """
    Return the load percentage of the room.
    This will be for letting the front end to know it can open up.
    Right now this is just phony data, TODO real loading.
    """
    percent = RedisKeys.API_LOAD_PERCENTAGE.get()
    percent = int(percent)
    new_percent = percent + 10
    if new_percent > 100:
        new_percent = 100
    RedisKeys.API_LOAD_PERCENTAGE.set(str(new_percent))
    if new_percent == 100:
        RedisKeys.API_ROOM_STATUS.set("READY")
    return new_percent


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
    # This needs to tell all the pis to reset, wait for them to reset,
    # The reset itself.
    # pi_node_controller.reset_all()
    # Timer().reset()
    # Also restart the API, lowkey.
    return "Room Reset"

@app.route("/stop", methods=["POST"])
def stop():
    """
    Stop the room.
    """
    Timer().stop()
    broadcast("stop")
    RedisKeys.API_ROOM_STATUS.set("STOPPED")
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
    pi_nodes_dict = {}
    pi_nodes_dict["pi_nodes"] = pi_node_controller.get_serializable_pis()
    return jsonify(pi_nodes_dict)


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
