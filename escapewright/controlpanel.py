################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Create a control panel server
#     Updated: 25 OCT 2023
# Description: This class is intended to use in a script to create a control
#              panel server. The server will be used to control the raspberry pi
#              and the game. The server will be used to send commands to the
#              raspberry pi, and to receive data from the raspberry pi.
#              This is not a runnable script.
#
################################################################################

import os                                # Used to get the path to the templates
from flask import Flask                  # Used to create the flask app
from flask import render_template        # Used to render the HTML
from flask import jsonify                # Used to send JSON data
import socket                            # Used to get the local IP address
from .timer import Timer                 # Used to create the timers
import datetime                          # Used to get the current time
import subprocess                        # Used to run the shell commands
import logging                           # Used to log the program
import time                              # Used to sleep the program
import threading                         # Used to run some tasks in a thread
import markdown

# Class Functions
#   get_local_ip() - Get the local IP address, not intended to use outside of the class
#   define_routes() - Define the routes for the flask app
#   run() - Run the flask app

# Flaskapp Routes
#   index - The index page
#   start - Start the room
#   reset - Reset the room
#   stop - Stop the room
#   failed - The room has failed
#   hard_reset - Hard reset the room
#   trigger - Trigger a message
#   update_status - Update the status of a specific client
#   generate_css - Generate the CSS for the pages

class ControlPanel:
    def __init__(self, room, script, overrides, column1, column2, client_controller, site_folder_path, logger, room_length=60, reset_time=2.5, port=12413):
        self.host = self.get_local_ip()             # Set the local IP
        self.port = port                            # Set the port 
        self.room = room                            # Set the room name
        self.room_timer = Timer(room_length)        # Create the timer for the room
        self.reset_timer = Timer(reset_time)        # Create the timer for the reset button
        self.client_controller = client_controller  # Set the client controller
        self.flaskapp = Flask(__name__)             # Create the flask app
        self.flaskapp.static_folder = os.path.join(site_folder_path, 'static')
        self.flaskapp.template_folder = os.path.join(site_folder_path, 'templates')

        self.logger = logger                        # Set the logger

        self.getting_statuses = False               # Set the getting statuses flag to false
        self.last_reset = datetime.datetime.now()   # Set the last reset time to now
        self.load_check = 0
        self.status_checks = 0
        self.MAX_CHECKS = 3
        self.check_status = None
        self.load_error = False
        
        self.load_percentage = 0

        self.column1 = column1 
        self.column2 = column2

        self.script = script
        self.overrides = overrides

    def get_local_ip(self):
        # UDP Connection, No data sent
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        try:
            s.connect(('10.255.255.255', 1)) # Connect to the broadcast address
            ip = s.getsockname()[0]          # Get the IP
        except Exception:
            ip = '127.0.0.1'                 # If it fails, use localhost
        finally:
            s.close()                        # Close the socket
        return ip                            # Return the ip
    
    def define_routes(self):
        # Homepage
        @self.flaskapp.route('/')
        def index():
            loading = True
            # If the room is running, show the index page 
            if self.room_timer.start_time != None:
                loading = False
                return self.render_index(loading)
            
            # If the room is ready, show the index page
            if self.client_controller.all_ready():
                loading = False
                return self.render_index(loading)

            # If the room is not ready, show the loading curtain.
            load_thread = threading.Thread(target=self.load_room)
            load_thread.start()
            return self.render_index()
        
        @self.flaskapp.route('/start')
        def start():
            # Start the room
            return
        
        @self.flaskapp.route('/reset')
        def reset():
            # Reset the room after the user confirms
            self.reset_self()
            self.client_controller.reset()
            return
        
        @self.flaskapp.route('/stop')
        def stop():
            # Stop the room
            # Get confirmation from the user, then stop the room
            # This will likely require a hard reboot
            return
        
        @self.flaskapp.route('/failed')
        def failed():
            # The players have failed, start the fail sequence.
            return

        @self.flaskapp.route('/hard_reset')
        def reboot():
            # Something wrong happened, hard reset everything
            if not self.client_controller.reboot_all():
                self.client_controller.force_reboot_failed()
            subprocess.run(["sudo", "reboot"])
            return

        @self.flaskapp.route('/trigger/<message>')
        def trigger(message):
            # Receive a trigger and relay it to all the clients
            self.client_controller.broadcast(message)
            return
        
        @self.flaskapp.route('/update_status/<name>/<message>')
        def update_status(name, message):
            self.client_controller.update_status(name, message)
            return "Status Updated"
        
        @self.flaskapp.route('/detect_change')
        def detect_change():
            if self.client_controller.detect_change():
                return "True"
            return "False"
        
    def render_index(self, loading = True):
        # Render the index page

        # Split the clients by column
        clients_column1 = self.clients_by_location(self.column1) 
        clients_column2 = self.clients_by_location(self.column2)

        # Convert Script
        script_html = self.script_to_html()

        return render_template('index.html', 
                               name=self.room,
                               loading=loading, 
                               column1_name=self.column1,
                               column2_name=self.column2,
                               column1=clients_column1,
                               column2=clients_column2,
                               script_html=script_html)
    
    def clients_by_location(self, location):
        clients = []
        for client in self.client_controller.clients:
            if client.location == location:
                clients.append(client)
        return clients
    
    def load_room(self):
        if self.getting_statuses: 
            self.log("Already getting statuses", "DEBUG")
            return False
        
        if self.MAX_CHECKS == self.status_checks:
            self.log("Max checks reached, Refresh Page Needed", "WARNING")
            self.status_checks = 0
            self.load_error = True
            return

        self.getting_statuses = True

        if self.room_timer.start_time != None:
            self.log("Room already running, no load needed", "DEBUG")
            self.getting_statuses = False
            return False
        
        if self.client_controller.all_ready():
            self.log("All clients ready", "INFO")
            self.load_percentage = 100
            self.getting_statuses = False
            return True
        
        for client in self.client_controller.clients:
            print(f"Checking {client.name}, load percentage: {self.load_percentage}")
            if client.status == "READY":
                self.log(f"{client.name} is ready, skipping recheck", "DEBUG")
                continue

            client.get_status()
            print(f"Status of {client.name}: {client.status}")
            if client.status == "READY":
                self.load_percentage += (100 / len(self.client_controller.clients))
            time.sleep(1)
        
        if self.client_controller.all_ready():
            self.log("All clients ready", "INFO")
            self.getting_statuses = False
            return True
        else:
            self.status_checks += 1
            self.log(f"Not all clients ready, checking again. Attempt {self.status_checks}", "WARNING")
            self.getting_statuses = False
            return self.load_room() 
    
    def reset_self(self):
        self.load_percentage = 0.0
        self.room_timer.reset()
        self.last_reset = datetime.datetime.now()
        self.status_checks = 0
        self.load_percentage = 0
        self.load_error = False
    
    def script_to_html(self):
        # read the script file into a string
        script_data = ""
        with open(self.script, 'r') as f:
            script_data = f.read()
        
        # Convert that string to html with markdown
        html = markdown.markdown(script_data)
        return html

    def run(self):
        self.define_routes()
        # self.client_controller.print_all_data()
        self.flaskapp.run(host=self.host, port=self.port)
        return
    
    def log(self, message, level=None):
        if self.logger == None: 
            print(message)
            return
        
        if level == None:
            self.logger.info(message)
        elif level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.error(message)
        else:
            self.logger.info(message)
        return