################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Connection between control panel, and each pi role
#     Updated: 09 NOV 2023
# Description: 
#              
################################################################################

# External Imports
from flask import Flask            # Flask is the web server
from flask import render_template  # Render HTML templates
from flask import request          # For getting the incoming IP
from threading import Timer        # Timer for rebooting
from typing import Type            # Type hinting
import socket                      # For getting the local IP
import subprocess                  # For rebooting
import os                          # For getting the path to the site folder
import datetime                    # For getting the uptime

# Internal Imports
from .escapiclient import EscapiClient
from .role import Role
from .escapitransmitter import EscapiTransmitter

class EscapiServer:
    def __init__(self, name, role: Type[Role], site_folder_path, location="N/A", port=12413, logger=None):
        self.name = name                 # Name of the Pi
        self.location = location         # Location of the Pi
        self.port = port                 # Port of the Pi, ETA uses 12413
        self.role = role                 # This is the class that is the pi's purpose
        self.logger = logger             # Logger
        self.role.set_observer(self)     # Add this server as an observer to the role
        self.ip = self.get_local_ip()    # IP of the Pi
        self.transmitter = EscapiTransmitter(self.name, self.location, self.port)
        self.status = "BOOTING"          # Status of the Pi
        self.last_relay = "N/A"          # Last relayed message
        self.last_reset = "N/A"          # Last reset
        self.last_reboot = datetime.datetime.now()# Last reboot

        self.flaskapp = Flask(__name__)  # Flask app
        self.flaskapp.static_folder = os.path.join(site_folder_path, 'static')
        self.flaskapp.template_folder = os.path.join(site_folder_path, 'templates')

        self.logger.debug(f"Server Class Created")
        self.logger.debug(f"Server info: {self.name}")
        self.logger.debug(f"           : {self.location}")
        self.logger.debug(f"           : {self.port}")
        self.logger.debug(f"           : {self.ip}")
        return
    
    def get_local_ip(self):
        # UDP Connection, No data sent
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        try:
            s.connect(('10.255.255.255', 1)) # Connect to the broadcast address
            ip = s.getsockname()[0]          # Get the IP
            self.log(f"Local IP set to: {ip}", "DEBUG")
        except Exception:
            ip = '127.0.0.1'                 # If it fails, use localhost
            self.log(f"Local IP failed to set, using localhost { ip }", "ERROR")
        finally:
            s.close()                        # Close the socket
        
        return ip                            # Return the ip
    
    def define_routes(self):
        self.log(f"Defining Routes:", "DEBUG")
        self.log(f"index, relay, status, start, override, reset, stop, reboot, logs", "DEBUG")
        @self.flaskapp.route('/')
        def index():
            visit_ip = request.remote_addr
            self.log(f"Index Visited by {visit_ip}", "INFO")
            last_reboot = self.last_reboot.strftime("%m/%d @ %H:%M:%S")
            uptime = self.get_uptime() 
            return render_template('index.html', 
                                   name=self.name, 
                                   status=self.status,
                                   ip=self.ip,
                                   last_relay=self.last_relay,
                                   last_reset=self.last_reset,
                                   last_reboot=last_reboot,
                                   uptime=uptime)
        
        @self.flaskapp.route('/relay/<message>', methods=['GET'])
        def relay(message):
            try:
                if message:
                    if self.role.process_message(message):
                        self.log(f"Relay: {message}, Event Activated", "INFO")
                    else:
                        self.log(f"Relay: {message}, Event Not Activated", "INFO")
            except Exception as e:
                self.log(f"Relay: {message} failed to process", "ERROR")
                return 'Error processing message', 500 
       
        @self.flaskapp.route('/status')
        def status():
            self.log(f"Status Requested, current status is: {self.status}", "DEBUG")
            return str(self.status)
         
        @self.flaskapp.route('/start/', defaults={'option': None})
        @self.flaskapp.route('/start/<option>/')
        def start(option):
            function = self.role.start
            function_name = "Start"
            return self.task_responses(function, option, function_name)

        @self.flaskapp.route('/override/', defaults={'option': None})
        @self.flaskapp.route('/override/<option>/')
        def override(option):
            function = self.role.override
            function_name = "Override"
            return self.task_responses(function, option, function_name)


        @self.flaskapp.route('/reset/', defaults={'option': None})
        @self.flaskapp.route('/reset/<option>/')
        def reset(option):
            function = self.role.reset
            function_name = "Reset"
            return self.task_responses(function, option, function_name)

        @self.flaskapp.route('/stop/', defaults={'option': None})
        @self.flaskapp.route('/stop/<option>/')
        def stop(option):
            function = self.role.stop
            function_name = "Stop"
            return self.task_responses(function, option, function_name)
        
        
        @self.flaskapp.route('/reboot/', defaults={'option': None})
        @self.flaskapp.route('/reboot/<option>/')
        def reboot(option):
            # Reboot the pi after 5 seconds
            delay = 5
            reboot_timer = Timer(delay, self.reboot_command)
            reboot_timer.start()
            self.logger.info("Received Reboot Request")
            if option == "self":
                return self.confirmation(f"Rebooting in {delay} seconds")
            return f"Rebooting in {delay} seconds", 200
        
        @self.flaskapp.route('/add_to_control_panel')
        def add_to_control_panel():
            # Create a client to pass onto the transmitter
            client = EscapiClient(self.name, self.ip, self.port)
            self.transmitter.add_self(client)

        @self.flaskapp.route('/logs')
        def logs():
            return 'LOGS NOT IMPLEMENTED', 200
    
    def load_role(self):
        self.log(f"Loading Role: {self.role}", "DEBUG")
        return self.role.load()
    
    def reboot_command(self):
        subprocess.run(['sudo', 'reboot', 'now'])
    
    def update_status(self, status):
        self.status = status
        self.transmitter.update_status(status)
        self.logger.info(f"Status Updated: {status}")
        return
    
    def get_uptime(self):
        uptime = datetime.datetime.now() - self.last_reboot
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_uptime = f"{days}d {hours}h {minutes}m {seconds}s"
        self.logger.debug(f"Uptime Calculated: {formatted_uptime}")
        return formatted_uptime
    
    def trigger(self, event):
        self.transmitter.trigger(event)
        self.logger.info(f"Triggered event: {event}")    
        return
    
    def log(self, message, level=None):
        if self.logger == None: return
        
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
    
    def task_responses(self, function, option, request_name):
        run = function
        success = run()

        self.log(f"{ request_name } Requested, current status is: {self.status}", "INFO")

        if success: 
            message = f"{request_name} successful"
        else:
            message = f"{request_name} failed, see logs for details"

        self.log(f"{message}", "INFO")

        # If the request was sent via the dashboard, return the confirmation page
        if option == "self":
            return self.confirmation(message)
        
        # If the request was sent via the control panel, return answer
        if success:
            return message, 200
        return message, 500
    
    def confirmation(self, message):
        return render_template('message.html',
                               name = self.name,
                               message = message)

    def run(self):
        self.load_role()
        self.define_routes()
        self.log(f"Server started on {self.ip}:{self.port}", "INFO")
        self.flaskapp.run(host=self.ip, port=self.port)
        return