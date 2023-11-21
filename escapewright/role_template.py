################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Template for roles, which could be puzzles, maestro, or pretty
#              much anything else.
#     Updated: 20 NOV 2023 
# Description: 
#              
################################################################################

from .role import Role
import threading
from time import sleep

# Inherited functions
# trigger_event(event) - Trigger an event 
# update_status(status) - Update the status of the role
# log(message, level) - Log a message to the logger
# join_thread() - Join the thread


class RoleTemplate(Role):
    def __init__(self, logger = None):
        self.EASY_RESET_STATUSES = ["COMPLETE", "STOPPED", "BYPASSED"]

        self.observer = None    # Inherited from Role
        self.status = None      # Inherited from Role
        self.running = False    # Inherited from Role
        self.logger = logger    # Inherited from Role
        self.role_thread = None

        # trigger format is { "trigger": function }
        self.triggers = { "load": self.load,
                          "start": self.start,
                          "reset": self.reset,
                          "stop": self.stop,

                          }

        ### Unique Members ###
        # trigger format is { "trigger": function }
        unique_triggers = {"bypass": self.bypass}
        self.triggers.update(unique_triggers)

        # Add any unique members here
        return

    def load(self):
        self.update_status("READY")
        self.is_resetting = False
        return True
    
    def start(self):
        if self.running:
            self.log("Role Thread already running", "ERROR")
            return False

        self.update_status("ACTIVE")
        self.log("Role Thread Started", "INFO")
        self.role_thread = threading.Thread(target=self.logic)
        self.role_thread.start()
        return True
    
    def logic(self):
        self.running = True
        # This is the main function for the puzzle
        # It should be called in a thread
        while self.running:
            print("Looping")
            sleep(1)
        return
    
    def reset(self):
        self.log(f"Reset Requested", "DEBUG")
        if self.status == "READY":
            return True

        if self.status in self.EASY_RESET_STATUSES:
            return self.load()

        if self.force_join_thread(): 
            return self.load()
        return False
    
    def stop(self):
        self.update_status("STOPPED")
        self.force_join_thread() 
        return
    
    def bypass(self):
        self.update_status("BYPASSED")
        self.force_join_thread()
        return