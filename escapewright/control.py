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

class Control:
    def __init__(self, host, port, room):
        self.host = host
        self.port = port
        self.room = room
        self.flaskapp = Flask(__name__)  # Create the flask instance