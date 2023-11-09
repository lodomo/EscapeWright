################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: For a Raspberry Pi to serve data to the control panel
#     Updated: 01 NOV 2023
# Description: 
#              
################################################################################

# External Imports
from flask import Flask            # Flask is the web server
from flask import render_template  # Render HTML templates
from threading import Timer        # Timer for rebooting
from typing import Type            # Type hinting
import socket                      # For getting the local IP
import subprocess                  # For rebooting
import os
import datetime

# Internal Imports
from .escapiclient import EscapiClient
from .role import Role
from .escapitransmitter import EscapiTransmitter

class EscapiServer:
    def __init__(self, name, role: Type[Role], site_folder_path, location="N/A", port=12413):
        self.name = name                 # Name of the Pi
        self.location = location         # Location of the Pi
        self.port = port                 # Port of the Pi, ETA uses 12413
        self.role = role                 # This is the class that is the pi's purpose
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
        return
    
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
        @self.flaskapp.route('/')
        def index():
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
                    self.role.process_message(message)
            except Exception as e:
                return 'Error processing message', 500 
       
        @self.flaskapp.route('/status')
        def status():
            return str(self.status)
         
        @self.flaskapp.route('/start/', defaults={'option': None})
        @self.flaskapp.route('/start/<option>/')
        def start(option):
            if option == "self":
                return 'START SELF NOT YET IMPLEMENTED', 200
            return 'ROLE NOT STARTED NOT YET IMPLEMENTED', 200
        
        @self.flaskapp.route('/override')
        def override():
            return 'OVERRIDE NOT STARTED NOT YET IMPLEMENTED', 200
        
        @self.flaskapp.route('/reset')
        def reset():
            return 'RESET NOT STARTED NOT YET IMPLEMENTED', 200
        
        @self.flaskapp.route('/reboot')
        def reboot():
            # # Reboot the pi after 5 seconds
            # delay = 5
            # reboot_timer = Timer(delay, self.reboot_command)
            # reboot_timer.start()
            return "REBOOT NOT STARTED NOT YET IMPLEMENTED", 200
        
        @self.flaskapp.route('/add_to_control_panel')
        def add_to_control_panel():
            # Create a client to pass onto the transmitter
            client = EscapiClient(self.name, self.ip, self.port)
            self.transmitter.add_self(client)

        @self.flaskapp.route('/logs')
        def logs():
            return 'Logs'
    
    def load_role(self):
        return self.role.load()
    
    def reboot_command():
        subprocess.run(['sudo', 'reboot', 'now'])
    
    def update_status(self, status):
        self.status = status
        self.transmitter.update_status(status)
        return
    
    def relay(self, message):
        try:
            if message:
                self.role.process_message(message)
                return True
        except Exception as e:
            return False
    
    def get_uptime(self):
        uptime = datetime.datetime.now() - self.last_reboot
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_uptime = f"{days}d {hours}h {minutes}m {seconds}s"
        return formatted_uptime
    
    def trigger(self, event):
        self.transmitter.trigger(event)
        return
    
    def start_server(self):
        self.load_role()
        self.define_routes()
        self.flaskapp.run(host=self.ip, port=self.port)
        return