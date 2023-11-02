################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: For a Raspberry Pi to serve data to the control panel
#     Updated: 01 NOV 2023
# Description: 
#              
################################################################################

# External Imports
from flask import Flask
from threading import Timer
from typing import Type
import socket
import subprocess

# Internal Imports
from .escapiclient import EscapiClient
from .role import Role
from .escapitransmitter import EscapiTransmitter

class EscapiServer:
    def __init__(self, name, role: Type[Role], transmitter: Type[EscapiTransmitter], location="N/A", port=12413):
        self.name = name                 # Name of the Pi
        self.location = location         # Location of the Pi
        self.port = port                 # Port of the Pi, ETA uses 12413
        self.transmitter = transmitter   # This is the class that sends messages to the control panel
        self.role = role                 # This is the class that is the pi's purpose
        self.role.set_observer(self)     # Add this server as an observer to the role
        self.ip = self.get_local_ip()    # IP of the Pi
        self.status = "BOOTING"          # Status of the Pi
        self.flaskapp = Flask(__name__)  # Flask app
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
            # return render_template('index.html', pi_name=self.name, status=self.status)
            return "IT WORKS!"
        
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
        
        @self.flaskapp.route('/reboot')
        def reboot():
            # Reboot the pi after 5 seconds
            delay = 5
            reboot_timer = Timer(delay, self.reboot_command)
            reboot_timer.start()
            return "Reboot initiated", 200
        
        @self.flaskapp.route('/add_to_control_panel')
        def add_to_control_panel():
            # Create a client to pass onto the transmitter
            client = EscapiClient(self.name, self.ip, self.port)
            self.transmitter.add_self(client)
    
    def reboot_command():
        subprocess.run(['sudo', 'reboot', 'now'])
    
    def update_status(self, status):
        self.status = status
        self.transmitter.update_status(status)
        return
    
    def trigger(self, event):
        self.transmitter.trigger(event)
        return
    
    def start_server(self):
        self.define_routes()
        self.flaskapp.run(host=self.ip, port=self.port)
        return