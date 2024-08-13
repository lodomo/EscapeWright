###############################################################################
#        ______  _____  _____          _____  ______
#       |  ____|/ ____|/ ____|   /\   |  __ \|  ____|
#       | |__  | (___ | |       /  \  | |__) | |__
#       |  __|  \___ \| |      / /\ \ |  ___/|  __|
#       | |____ ____) | |____ / ____ \| |    | |____
#       |______|_____/ \_____/_/____\_\ |____|______|_    _ _______
#                   \ \        / /  __ \|_   _/ ____| |  | |__   __|
#                    \ \  /\  / /| |__) | | || |  __| |__| |  | |
#                     \ \/  \/ / |  _  /  | || | |_ |  __  |  | |
#                      \  /\  /  | | \ \ _| || |__| | |  | |  | |
#                       \/  \/   |_|  \_\_____\_____|_|  |_|  |_|
# ------------------------------------------------------------------------------
#
# Author: Lorenzo D. Moon (Lodomo.Dev)
# Date: 04 APR 2024
# Purpose: API for the Control Console, and Human Interface to the Client Pis.
# Description: Creates a server for the client pi to communicate with the
#              control console. It also provides a gui interface for someone
#              to directly interact with the client pi, and retrieve logs.
#
###############################################################################

# External Imports
import datetime
import logging
import os
import subprocess
from threading import Timer as ThreadTimer
import sys

from flask import Flask  # Flask is the web server
from flask import render_template  # Render HTML templates
from flask import request  # For getting the incoming IP

# Internal Imports
from .observer import Observer
from .role import Role
from .transmitter import Transmitter
from .utils import is_valid_ip as utils_is_valid_ip


class Client(Observer):
    def __init__(self, data: dict = None):
        super().__init__(data)  # Set up the observer

        try:
            self.__name = data["name"]
            self.__location = data["location"]
            self.__port = data["port"]
            self.__role = data["role"]
            self.__ip = data["ip"]
        except KeyError as e:
            logging.error(f"Missing key in data: {e}")
            raise

        self.__transmitter = Transmitter(data)

        self.__last_relay = None
        self.__last_reset = None
        self.__last_reboot = datetime.datetime.now() 
        self.__last_visit = None

        self.flaskapp = Flask(__name__)  # Flask app
        self.flaskapp.static_folder = os.path.join(
            data["site_path"], "static")
        self.flaskapp.template_folder = os.path.join(
            data["site_path"], "templates")
        return

    @property
    def name(self) -> str:
        return self.__name

    @property
    def location(self) -> str:
        return self.__location

    @property
    def port(self) -> int:
        return self.__port

    @property
    def role(self) -> Role:
        return self.__role

    @property
    def ip(self) -> str:
        return self.__ip

    @property
    def last_relay(self) -> str:
        return self.__last_relay

    @property
    def last_reset(self) -> datetime.datetime:
        return self.__last_reset

    @property
    def last_reboot(self) -> datetime.datetime:
        return self.__last_reboot

    @property
    def last_visit(self) -> datetime.datetime:
        return self.__last_visit

    def __set_last_visit(self) -> datetime.datetime:
        # Setter for the last visit time
        visit_ip = request.remote_addr
        logging.info(f"Visited by {visit_ip}")
        self.__last_visit = datetime.datetime.now()
        return self.last_visit

    def __set_last_reset(self) -> datetime.datetime:
        self.__last_reset = datetime.datetime.now()
        return self.last_reset

    def __set_last_relay(self, message) -> str:
        self.__last_relay = message
        return self.last_relay

    def __data_validation(self):
        # This function will throw errors if the incoming data is bad.
        # This should only matter during development of a new client
        # Because it will crash the program if the data is bad
        if not isinstance(self.__name, str):
            raise TypeError("Name must be a string")

        if not isinstance(self.__location, str):
            raise TypeError("Location must be a string")

        if not isinstance(self.__port, int):
            raise TypeError("Port must be an integer")
            if self.__port < 0 or self.__port > 65535:
                raise ValueError("Port must be between 0 and 65535")

        if not isinstance(self.__role, Role):
            raise TypeError("Role must be a Role object")

        if not utils_is_valid_ip(self.__ip):
            raise ValueError("IP must be a valid IPv4 or IPv6 address")
        return

    def __define_routes(self):
        logging.debug("Defining Routes")

        @self.flaskapp.route("/")
        def index():
            # Index defined outside of the define_routes function
            return self._index()

        @self.flaskapp.route("/relay/<message>", methods=["GET"])
        def relay(message):
            return self.__relay(message)

        @self.flaskapp.route("/status")
        def status():
            return str(self.role.status), 200

        @self.flaskapp.route("/start/", defaults={"option": None})
        @self.flaskapp.route("/start/<option>/")
        def start(option):
            return self.__task_responses("start", option)

        @self.flaskapp.route("/bypass/", defaults={"option": None})
        @self.flaskapp.route("/bypass/<option>/")
        def bypass(option):
            return self.__task_responses("bypass", option)

        @self.flaskapp.route("/reset/", defaults={"option": None})
        @self.flaskapp.route("/reset/<option>/")
        def reset(option):
            return self.__task_responses("reset", option)

        @self.flaskapp.route("/stop/", defaults={"option": None})
        @self.flaskapp.route("/stop/<option>/")
        def stop(option):
            return self.__stop(option)

        @self.flaskapp.route("/reboot/", defaults={"option": None})
        @self.flaskapp.route("/reboot/<option>/")
        def reboot(option):
            return self.__reboot(option)

    def __show_curtain(self):
        delay = 5 * 60  # Seconds 

        # If it's the first visit, show the curtain
        if self.__last_visit is None:
            return True

        # If it's been >5 mins since the last visit, show the curtain
        if (datetime.datetime.now() - self.__last_visit).seconds > delay:
            return True

        return False

    def _index(self):
        show_curtain = self.__show_curtain()

        last_reboot = self.last_reboot.strftime("%m/%d @ %H:%M")

        last_reset = self.last_reset
        if last_reset is None:
            last_reset = "N/A"
        else:
            last_reset = self.last_reset.strftime("%m/%d @ %H:%M")

        uptime = self.__get_uptime()
        logs = self.__generate_logs()

        self.__set_last_visit()  # Log the visit, and update the last visit time

        return render_template(
            "index.html",
            name=self.name,
            status=self.role.status,
            ip=self.ip,
            last_relay=self.last_relay,
            last_reset=last_reset,
            last_reboot=last_reboot,
            uptime=uptime,
            logs=logs,
            show_curtain=show_curtain,
        )

    def __relay(self, message):
        try:
            if message:
                self.__set_last_relay(message)
                if self.role.process_message(message):
                    logging.info(f"Relay: {message}, Event Activated")
                else:
                    logging.debug(f"Relay: {message}, Event Not Activated")
                return "Message Processed", 200
        except Exception:
            logging.error(f"Relay: {message} failed to process")
            return "Error processing message", 500

    def __status(self):
        logging.debug(f"Status Requested, status is: {self.role.status}")

    def __stop(self, option):
        return self.__task_responses("stop", option)

    def __reboot(self, option):
        # Reboot the pi after 5 seconds
        delay = 5
        reboot_timer = ThreadTimer(delay, self.__reboot_command)
        reboot_timer.start()
        visit_ip = request.remote_addr
        logging.info(f"Received reboot request from {visit_ip}")
        if option == "self":
            return self.__confirmation(f"Rebooting in {delay} seconds")
        return f"Rebooting in {delay} seconds", 200

    def __load_role(self):
        # Prepare the role to be ran. This function should be called before
        # the server is started or else the role will never load
        logging.info(f"Loading Role: {self.role}")
        return self.role.load()

    def __reboot_command(self):
        subprocess.run(["sudo", "reboot", "now"])

    def __transmit_status(self):
        logging.info(f"Transmitting Status: {self.role.status}")
        self.transmitter.update_status(self.role.status)
        return

    def __get_uptime(self):
        uptime = datetime.datetime.now() - self.last_reboot
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_uptime = f"{days}d {hours}h {minutes}m {seconds}s"
        logging.debug(f"Uptime Calculated: {formatted_uptime}")
        return formatted_uptime

    def __trigger(self, event):
        self.transmitter.trigger(event)
        logging.info(f"Triggered event: {event}")
        return

    def __task_responses(self, request, option):
        logging.info(f"Forced {request} Requested")
        success = self.role.process_message(request)
        response = None

        if success:
            response = f"{request} request successful", 200
        else:
            response = f"{request} request failed", 500

        if option == "self":
            # If the request was sent via the dashboard,
            # return the confirmation page to the user
            return self.__confirmation(request, success)
        return response

    def __confirmation(self, message, is_error=False):
        # Return the confirmation page to the user.
        # This is an INTERNAL page, and should not be accessed by the control
        # panel. This is just if you have to directly interact with the pi
        return render_template(
            "message.html", name=self.name, message=message, is_error=is_error
        )

    def __generate_logs(self):
        # Grab the logs from the root logger and return them as a list.
        # This list will then be handled by javascript on the front end
        root_logger = logging.getLogger()
        log = []

        if root_logger is None:
            log.append("No logs found")
            return log

        log_file = root_logger.handlers[0].baseFilename

        with open(log_file, "r") as f:
            for line in f:
                log.insert(0, line)
        return log

    def run(self):
        self.__load_role()
        self.__define_routes()
        logging.info(f"Client {self.name} started on {self.ip}:{self.port}")
        self.flaskapp.run(host=self.ip, port=self.port)
        return
