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

#### TODO SETUP LOGGER

class EscapiClientController:
    def __init__(self, filename, logger = None):
        self.filename = filename
        self.clients = self.load_clients()
        self.logger = logger
    
    def get_statuses(self):
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

    def reboot_all(self):
        success = True
        for client in self.clients:
            if not client.reboot():
                success = False
                client.status = "REBOOT FAILED"
                self.errors.append(f"Failed to hard reset {client.name}")
        return success
    
    def stop_all(self):
        success = True
        for client in self.clients:
            if not client.stop():
                success = False
                self.errors.append(f"Failed to stop {client.name}")
        return success
    
    def force_reboot_on_failed(self):
        sent_reboot = False
        for client in self.clients:
            if client.status == "REBOOT FAILED":
                client.status == "REBOOT FORCED"
                client.force_reboot()
                sent_reboot = True
        return sent_reboot
    
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
        for client in self.clients:
            client.relay(message)
    
    def update_status(self, client_name, message):
        client = self.find_client(client_name)
        if client:
            return client.update_status(message)
        return False
    
    def load_clients(self):
        client_list = []
        client_info = {}
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    if client_info:
                        client_list.append(EscapiClient(**client_info))
                        client_info = {}
                else:
                    key, value = line.split(':')
                    client_info[key.strip()] = value.strip()
            if client_info:
                client_list.append(EscapiClient(**client_info))
        return client_list
    
    def print_all_data(self):
        for client in self.clients:
            client.print_data()
        return
    
    def print_simple_data(self):
        print()
        print(f"**Client List**")
        for client in self.clients:
            client.print_simple()
        print(f"**End of Client List**")
        print()
        return