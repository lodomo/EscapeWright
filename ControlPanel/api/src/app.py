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
import time

import markdown
from flask import Flask, jsonify
from flask_cors import CORS
from src.pi_node import PiNodeController
from src.redis_keys import RedisKeys
from src.timer import Timer  # Treated as a global Timer()
from src.yaml_reader import open_yaml_as_dict

app = Flask(__name__)
CORS(app)
config = open_yaml_as_dict(RedisKeys.API_YAML_CONFIG.get())
worker_key = RedisKeys.API_WORKER_ID.get_then_increment()
pi_node_controller = PiNodeController(config["pi_nodes"])


@app.route("/")
def home():
    """
    This should be a mini api interface just to make
    sure everything works.
    """
    html = "<p>API Interface</p>"
    html += f"<p>Worker Key: {worker_key}</p>"
    html += f"<p>Up Time: {uptime()}</p>"
    return html, 200


###############################################################################
#                            Client Endpoints                                 #
###############################################################################


@app.route("/fetch/all", methods=["GET"])
def fetch_all():
    """
    Return all the data to the requester.
    This is used to initialize the front end.
    """
    return jsonify(generate_full_payload()), 200


@app.route("/fetch/dynamic", methods=["GET"])
def fetch_dynamic():
    """
    Return the dynamic data to the requester.
    This is data that may change after the server has started.
    """
    return jsonify(generate_dynamic_payload()), 200


@app.route("/fetch/static", methods=["GET"])
def fetch_static():
    """
    Return the static data to the requester.
    This is data that will not change after the server has started.
    """
    return jsonify(generate_static_payload()), 200


@app.route("/fetch/<specific_data>", methods=["GET"])
def fetch_specific_data(specific_data):
    """
    Return a specific data payload for the room.
    This might be good to just call all the time and get the data you want.
    """
    full_payload = generate_full_payload()
    data = search_nested_dicts(full_payload, specific_data)
    if data is not None:
        return jsonify(data), 200
    else:
        return "Data Not Found", 404


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
        pi_node_controller.broadcast("room_start")
        return "Room Started"

    if not timer.is_paused:
        timer.pause()
        pi_node_controller.broadcast("pause")
        return "Room Paused"

    timer.resume()
    pi_node_controller.broadcast("resume")
    return "Room Resumed"


@app.route("/override/<trigger_name>", methods=["POST"])
def override_broadcast(trigger_name):
    """
    Set an override for the room.
    """
    pi_node_controller.broadcast(trigger_name)
    return "Not Implemented (Override Broadcast)", 501


@app.route("/override/<trigger_name>/<pi_name>", methods=["POST"])
def override_relay(trigger_name, pi_name):
    """
    Set an override for a specific Pi.
    """
    pi_node_controller.relay(pi_name, trigger_name)
    return "Not Implemented (Override Relay)", 501


@app.route("/reset", methods=["POST"])
def reset():
    print("SIMULATING RESET SINCE NO PIS ARE CONNECTED")
    pi_node_controller.broadcast("reset")
    return restart_api()


@app.route("/stop", methods=["POST"])
def stop():
    """
    Stop the room.
    """
    Timer().stop()
    pi_node_controller.broadcast("stop")
    RedisKeys.API_ROOM_STATUS.set("STOPPED")
    return fetch_dynamic()


@app.route("/restart_api", methods=["POST"])
def restart_api():
    """
    Restart the server.
    This might be useful outside of "reset" but I doubt it.
    This probably breaks everything if you do it while the room is running.
    """
    pid = RedisKeys.GUNICORN_PID.get()
    print(f"Restarting server with PID: {pid}")
    os.system(f"kill -HUP {pid}")
    return fetch_all()


###############################################################################
#                             Node Endpoints                                  #
###############################################################################


@app.route("/trigger/", defaults={"message": "None"})
@app.route("/trigger/<message>", methods=["POST"])
def trigger(message):
    """
    This is technically identical to "override_broadcast" but it's the pi
    nodes alerting the server of a trigger, rather than the front end trying
    to bypass a problem or manually setting the state of something.
    """
    pi_node_controller.broadcast(message)
    return f"Triggered: {message}", 200


@app.route("/update_status/<pi_name>/<status>", methods=["POST"])
def update_status(pi_name, status):
    """
    Update the status of a Pi.
    """
    pi_node_controller.update_status(pi_name, status)
    return f"Updated Status: {pi_name} - {status}", 200


###############################################################################
#                             Helper Functions
###############################################################################


def generate_full_payload() -> dict:
    """
    Combine the two payloads into one, keep data divided.
    """
    payload = {}
    payload["dynamic"] = generate_dynamic_payload()
    payload["static"] = generate_static_payload()
    return payload


def generate_dynamic_payload() -> dict:
    """
    Generate the dynamic payload for the room.
    This is data that will likely change during the server's uptime.
    """
    payload = {}
    payload["load_percentage"] = load()
    payload["room_status"] = RedisKeys.API_ROOM_STATUS.get()
    payload["time_remaining"] = Timer().get_time()
    payload["pi_nodes"] = pi_node_controller.get_serializable_pis()
    return payload


def generate_static_payload():
    """
    Generate the static payload for the room.
    This is data that will not change between server restarts.
    """
    config = open_yaml_as_dict(RedisKeys.API_YAML_CONFIG.get())
    payload = {}
    payload["room_name"] = config["room_info"]["name"].upper()
    payload["last_boot"] = RedisKeys.API_LAST_BOOT.get()
    payload["overrides"] = generate_override_endpoints()
    payload["script"] = generate_script_html()
    return payload


def generate_script_html():
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


def generate_override_endpoints():
    return "TODO"


def search_nested_dicts(data: dict, key: str):
    """
    Search for a key in the data.
    """

    # Search for the key in the top level of the data
    for k, v in data.items():
        if k == key:
            return v

    # Dive deeper into the data
    for k, v in data.items():
        if isinstance(v, dict):
            result = search_nested_dicts(v, key)
            if result:
                return result
    return None


def uptime() -> str:
    """
    Return the uptime of the server.
    """
    last_boot = int(RedisKeys.API_LAST_BOOT.get())
    now = int(time.time())
    delta = now - last_boot

    YEAR = 31536000
    DAY = 86400
    HOUR = 3600
    MINUTE = 60

    years, remainder = divmod(delta, YEAR)
    days, remainder = divmod(remainder, DAY)
    hours, remainder = divmod(remainder, HOUR)
    minutes, seconds = divmod(remainder, MINUTE)

    formatted_time = ""
    if years:
        formatted_time += f"{years:02} years, "
    if days:
        formatted_time += f"{days:02} days, "
    formatted_time += f"{hours:02}h{minutes:02}m{seconds:02}s"

    return formatted_time


###############################################################################
#                                   Junk                                      #
###############################################################################


def load() -> int:
    """
    Return the load percentage of the room.
    This will be for letting the front end to know it can open up.
    Right now this is just phony data, TODO real loading.
    """
    print("WARNING THIS IS NOT A REAL LOAD PERCENTAGE")
    percent = RedisKeys.API_LOAD_PERCENTAGE.get()
    percent = int(percent)
    new_percent = percent + 10
    if new_percent > 100:
        new_percent = 100
    RedisKeys.API_LOAD_PERCENTAGE.set(str(new_percent))
    if new_percent == 100:
        RedisKeys.API_ROOM_STATUS.set("READY")
    return new_percent



def broadcast(message: str):
    """
    TODO
    """
    print("TODO BROADCAST")
    return


if __name__ == "__main__":
    app.run()
