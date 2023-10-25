################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: For a Control Server to interact with a Raspberry Pi server
#     Updated: 24 OCT 2023
# Description: This class is used to store all the information about a
#              Raspberry Pi server. It is used to store the name, ip, port,
#              address, status, and reachability of the server. It also has
#              functions to reset the server, and to get the status of the
#              server.
#
################################################################################

import requests
import subprocess
import ipaddress

class EscapiClient:
    # Initialize the Escapi 
    def __init__(self, name, ip_address, port, location):
        # Settable Members
        self.name = name                               # Name of the Pi
        self.ip = ip_address                           # IP of the Pi
        self.location = location                       # Location of the Pi
        self.port = port                               # Port of the Pi, ETA uses 12413
        self.address = f'http://{self.ip}:{self.port}' # Address of the Pi

        self.errors = []                               # Errors during validation 
        self.valid = self.validate()                   # Is the Escapi valid?

        # Status Members 
        self.reachable = False                         # Is the Pi reachable?
        self.status = "OFFLINE"                        # Status of the Pi
        self.status_was = "OFFLINE"                    # Status of the Pi last check 
    
    # Makes sure the initialization members are valid
    def validate(self):
        valid = True

        # Check if the name is a string
        if not isinstance(self.name, str):
            self.errors.append("Name must be a string.")
            valid = False
            
        # Check if the ip is a string
        if not isinstance(self.ip, str):
            self.errors.append("IP address must be a string.")
            valid = False
            
        # Check if the ip is a valid ip address
        try:
            ipaddress.ip_address(self.ip)
        except ValueError:
            self.errors.append(f"Invalid IP address for {self.name}")
            valid = False
        
        # Check if the location is a string
        if not isinstance(self.location, str):
            self.errors.append("Location must be a string.")
            valid = False

            
        # Check if the port is an integer
        if not isinstance(self.port, int) or not (10000 <= self.port <= 99999):
            self.errors.append("Port must be a 5-digit number.")
            valid = False
        
        return valid
    
    # Clear the Status of the Pi
    def clear_status(self):
        self.status = "OFFLINE"
        self.reachable = False 
    
    # Use a simple ping to see if the Pi is even reachable
    def reach(self):
        # If the pi has already been reached.
        if self.reachable:
            return self.reachable

        # See if the Flask-Server is down, or the whole pi is down.
        try:
            response = subprocess.run(["ping", "-c", "1", self.ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if response.returncode == 0:
                self.reachable = True
            else:
                self.reachable = False
        except Exception as e:
            print(f"An error occurred: {e}")
            self.reachable = False
        return self.reachable
    
    # Store the current pi status, and then get the current pi status
    def get_status(self):
        # print(f"Getting status of {self.name}...")
        self.status_was = self.status
        try:
            response = requests.get(self.address + "/status", timeout=10)
            if response.status_code == 200:
                last_word = response.text.split()[-1]
                self.status = last_word.upper()
                self.reachable = True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.status = "ERROR"
            self.reachable = False

        return self.reachable
    
    # Send a request to the pi to reset the Flask-Server
    def soft_reset(self): 
        self.status_was = self.status
        self.status = "RESETTING"
        try:
            response = requests.get(self.address + "/reset", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            self.status = "ERROR"
            return False
    
    # Send a request to the pi to reboot the whole pi. This is a last resort
    def hard_reset(self):
        # print(f"Hard resetting {pi.name}...")
        self.status = "REBOOTING"
        command = f'ssh lodomo@{self.ip} "sudo nohup reboot now &"'
        try:
            with open("/dev/null", "w") as fnull:
                subprocess.Popen(command, shell=True, stdout=fnull, stderr=fnull)
            # print(f"\033[92mSuccessfully hard reset {pi.name}\033[0m")
            return True
        except Exception as e:  # Popen doesn't raise CalledProcessError
            # print(f"\033[91mFailed to hard reset {pi.name}\033[0m")
            self.status = "REBOOT ERROR"
            print(f"An error occurred: {e}")
            return False
    
    # Convert the Escapi to a dictionary for JSON
    def to_dict(self):
        return {
            'name': self.name,
            'ip': self.ip,
            'location': self.location,
            'status': self.status,
            'status_was': self.status_was,
            'address': self.address
        }