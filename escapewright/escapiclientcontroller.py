################################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Check all the statuses of the Raspberry Pi Servers
# Description: This class uses builtin functions from EscapiClient that will check
#              the status of the Raspberry Pi Servers. It updates a list to
#              have a larger program (Control Console) handle what to do with
#              the statuses.
#              If initialized with "logging = True", it will log the statuses
#              to a file in the StatusTrackerLogs directory. It will log every
#              time program checks the statuses of the pis.
#              
################################################################################

from typing import List
from .escapiclient import EscapiClient

class EscapiClientController:
    def __init__(self, clients: List[EscapiClient]):
        self.clients = clients
    
    def if_print(self, message):
        if self.print_to_screen:
            print(message)
 
    def refresh_statuses(self):
        success = True
        for client in self.clients:
            if not client.get_status():
                success = False
        return success

    def reset_client(self, name):
        return self.find_client(name).reset()
    
    def reboot_client(self, name):
        return self.find_client(name).reboot()
    
    def reset_all(self):
        success = True
        for client in self.clients:
            if not client.reset():
                success = False
                self.errors.append(f"Failed to reset {client.name}")
        return success

    def full_hard_reset(self):
        success = True
        for client in self.clients:
            if not client.hard_reset():
                success = False
                self.errors.append(f"Failed to hard reset {client.name}")
        return success
    
    def all_ready(self):
        for client in self.clients:
            if client.status != "READY":
                return False
        return True
    
    def detect_change(self):
        for client in self.clients:
            if client.status != client.status_was:
                return True
        return False
    
    def get_serializable_pis(self):
        return [client.to_dict() for client in self.clients]
    
    def find_client(self, name):
        for client in self.clients:
            if client.name == name:
                return client 
        return None

    def clear_statuses(self):
        success = True
        for client in self.clients:
            if not client.clear_status():
                success = False
        return success
    
    def broadcast(self, message):
        for clients in self.clients:
            clients.relay(message)