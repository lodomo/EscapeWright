################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: For a Raspberry Pi to serve data to the control panel
#     Updated: 24 OCT 2023
# Description: 
#              
################################################################################
import threading
import requests
from .escapiclient import EscapiClient

class EscapiTransmitter:
    def __init__(self, name, control_ip, port=12413):
        self.name = name
        self.control_ip = control_ip
        self.port = port
        self.transmit_url = f"http://{self.control_ip}:{self.port}/trigger/"
        self.status_url = f"http://{self.control_ip}:{self.port}/update_status/"
        self.add_pi = f"http://{self.control_ip}:{self.port}/add_pi/"
    
    def send_request(url):
        try:
            requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to {url}: {e}")
        return

    def threaded_request(self, url):
        threading.Thread(target=self.send_request, args=(url,)).start()
        return "Request sent to " + url
    
    def trigger(self, message):
        url = self.transmit_url + message
        self.threaded_request(url)
        return
    
    def update_status(self, message):
        url = self.status_url + message
        self.threaded_request(url)
        return
    
    # Takes in a "EscapiClient" to add this pi to the control panel
    def add_self(self, escapiclient):
        # Deconstruct the escapiclient and push it to the control panel
        name = escapiclient.name            
        ip = escapiclient.ip                
        location = escapiclient.location    
        port = escapiclient.port            
        url = self.add_pi + f"{name}/{ip}/{location}/{port}" 
        self.threaded_request(url)
        return