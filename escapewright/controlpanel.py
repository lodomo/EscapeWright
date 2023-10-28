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

from flask import Flask
import socket
from .timer import Timer

class ControlPanel:
    def __init__(self, room, client_controller, room_length=60, reset_time=2.5, port=12413):
        self.host = self.get_local_ip()
        self.port = port
        self.room = room
        self.flaskapp = Flask(__name__)  # Create the flask instance
        self.room_timer = Timer(room_length)        # Create the timer for the room
        self.reset_timer = Timer(reset_time)    # Create the timer for the reset button
        self.client_controller = client_controller
    
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
            # Figure out which page is actually getting delivered
            #Logic of things to check....
            #If the timer is not running, then the room is not running..
            #If the statuses are all ready, then the room is ready
            #Else, there is an error
            return "Index Rendered"

        @self.flaskapp.route('/start')
        def start():
            # Start the room
            return
        
        @self.flaskapp.route('/reset')
        def reset():
            # Reset the room
            #Get confirmation from the user, then reset the room
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
        def hard_reset():
            # Something wrong happened, hard reset everything
            return

        @self.flaskapp.route('/trigger/<message>')
        def trigger(message):
            # Receive a trigger and relay it to all the clients
            return
        
        @self.flaskapp.route('/update_status/<name>/<message>')
        def update_status(message):
            # Receive a status update and update the status page
            return
        
    def run(self):
        self.define_routes()
        self.flaskapp.run(host=self.host, port=self.port)
        return