###############################################################################
# Description: Task Node API
# Version: 0.1
###############################################################################

import os
import time
import importlib

from flask import Flask, render_template
from flask_cors import CORS
from src.enums import Broadcasts
from src.yaml_reader import open_yaml_as_dict

config = open_yaml_as_dict("config.yaml")
print(config)
module_name = config["role"]["module"]
class_name = config["role"]["class"]
print(module_name, class_name)
module = importlib.import_module(f"src.{module_name}")
role_class = getattr(module, class_name)

app = Flask(__name__)
CORS(app)
role = role_class(config)
last_boot = time.time()


###############################################################################
#                                 Start Up                                    #
###############################################################################

role.load()

###############################################################################
#                              Basic Interface                                #
###############################################################################


@app.route("/")
def home():
    """
    Micro-Frontend for the Node API
    This gives you full power over the Node and is not intended for anyone
    but tech support to access.
    """
    payload = {}
    payload["status"] = role.status
    payload["uptime"] = uptime(last_boot)
    payload["last_boot"] = time.strftime(
        "%d %b %Y %H:%M:%S", time.localtime(int(last_boot))
    )
    
    payload["triggers"] = config["triggers"]

    return render_template("index.html", **payload)


###############################################################################
#                                Endpoints                                    #
###############################################################################


@app.route("/relay/<message>", methods=["POST"])
def relay(message):
    """
    Relay a message to the Node
    """
    message = message.upper()
    message = message.replace("-", "_")
    message = message.replace(" ", "_")

    # The only special non-role required message is reset.
    if message == Broadcasts.RESET:
        role.relay(Broadcasts.STOP)
        return restart_api()

    if message == Broadcasts.STOP:
        # Try "STOP" on the role, and do handling if it fails
        try:
            role.relay(Broadcasts.STOP)
            return f"Relay Received, Action Taken: {message}", 200
        except Exception as e:
            print(f"STOP FAILED: {e}")
            print("Restarting Server")
            return restart_api()

    action = role.relay(message)
    if action:
        return f"Relay Received, Action Taken: {message}", 200
    else:
        return f"Relay Received, No Action Taken: {message}", 200


@app.route("/status", methods=["GET"])
def status():
    """
    Return the status of the Node
    """
    return role.status, 200


@app.route("/restart_api", methods=["POST"])
def restart_api():
    """
    Restart the server.
    This might be useful outside of "reset" but I doubt it.
    This probably breaks everything if you do it while the room is running.
    """
    pid = get_pid()
    print(f"Restarting server with PID: {pid}")
    os.system(f"kill -HUP {pid}")
    return "Restarting Server", 200


###############################################################################
#                             Helper Functions
###############################################################################


def get_pid(file_name="./src/gunicorn.pid"):
    """
    Initialize the PID for the gunicorn server.
    This file is set from the gunicorn command line.
    --pid ./src/gunicorn.pid
    """
    try:
        with open(file_name, "r") as file:
            gunicorn_id = file.read()
        print(f"Gunicorn PID: {gunicorn_id}")
        return gunicorn_id
    except FileNotFoundError:
        print("No PID file found. Rerun with the --pid flag.")


def uptime(last_boot) -> str:
    """
    Return the uptime of the server.
    """
    now = int(time.time())
    delta = int(now - last_boot)

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
