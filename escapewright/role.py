################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Example Puzzle Class. This is a template for creating a puzzle
#     Updated: 20 NOV 2023 
# Description: 
#              
################################################################################

# *** DO NOT CHANGE THIS FILE ***
# Make a subclass of this class with the "role_template"
# This class ensures that the role_template is implemented correctly

### List of functions to implement
# load()     - Load the pi's role
# start()    - Start the pi's role
# reset()    - Reset the pi's role 
# stop()     - Stop the pi's role 
# bypass()   - Bypass the pi's current taskrole 

### List of inherited functions
# trigger_event(event)    - Trigger an event
# update_status(status)   - Update the status of the role
# log(message, level)     - Log a message to the logger
# join_thread()           - Join the thread
# can_start(status)    - Check if the role is startable
# can_bypass(status)   - Check if the role is bypassable

#### List of 'hidden' functions
# set_observer(observer) - Set the observer for this role
# process_message(message) - Process a message from the control panel

import threading
import datetime

class Role:
    def __init__(self, logger = None):
        self.EASY_RESET_STATUSES = ["COMPLETE", "STOPPED", "BYPASSED"]

        self.observer = None
        self.status = None
        self.running = False
        self.logger = logger
        self.is_resetting = False
        self.role_thread = None

        # trigger format is { "trigger": function }
        self.triggers = { "load": self.load,
                          "start": self.start,
                          "reset": self.reset,
                          "stop": self.stop}
        return
    
    def set_observer(self, observer):
        # Set the observer for this role, which is the piserver
        # Used for triggering events
        self.observer = observer
        return True  
    
    def trigger_event(self, event):
        # Event is a string. This tells the control panel what event
        # has been triggered
        if self.observer:
            self.observer.trigger(event)
            return True
        
        self.log("No observer set for role", "ERROR")
        return False
    
    def process_message(self, message):
        # Process a message from the control panel
        trigger_activated = False
        for trigger in self.triggers:
            if trigger in message:
                self.triggers[trigger]()
                trigger_activated = True
        return trigger_activated 
    
    def force_join_thread(self):
        if self.running:
            self.running = False
            if self.role_thread:
                self.role_thread.join()
                self.log("Role Thread Joined", "INFO")
            return True
        return False
    
    def update_status(self, status):
        # Update the status of the role. 
        self.status = status
        self.log(f"Status Updated: {self.status}", "INFO")
        if self.observer:
            self.observer.update_status()
        return
    
    def load(self):
        # Load the puzzle
        # This is time to prime the GPIO pins for whatever they're going to do
        self.log("No load function defined for empty role", "ERROR")
        return False
    
    def start(self):
        # Run whatever logic here for the puzzle to be solvable
        self.log("No start function defined for empty role", "ERROR")
        return False
    
    def reset(self):
        CAN_RESET_STATUSES = ["COMPLETE", "STOPPED", "BYPASSED"]
        self.log(f"Reset Requested", "DEBUG")

        # If the role is already ready, then no reset is needed
        if self.status == "READY":
            self.log("Already ready, if need to trouble shoot, use Reboot", "INFO")
            return True
        
        # Tell the observer that the role is resetting
        if self.observer != None:
            self.observer.last_reset = datetime.datetime.now()

        # If the role is already resetting, then no reset is needed
        if self.status in CAN_RESET_STATUSES:
            return self.load()

        # If the role is active, then we need to stop the thread
        if self.force_join_thread(): 
            return self.load()
        return False
    
    def stop(self):
        # Run whatever logic here for the puzzle to stop
        self.log("No stop function defined for empty role", "ERROR")
        return False
    
    def bypass(self):
        # Run whatever logic here for the puzzle to override
        self.log("No override function defined for empty role", "ERROR")
        return False
    
    def can_start(self, status):
        if self.running:
            self.log("Role Thread already running", "ERROR")
            return False

        if self.status != "READY":
            self.log("Cannot Start Role Thread from this status. Reset Required", "ERROR")
            return False
        return True

    def can_bypass(self, status):
        if self.status == "BYPASSED":
            self.log("Role already bypassed", "ERROR")
            return False
        
        if self.status == "READY":
            self.log("Role not started yet, can only bypass when active", "ERROR")
            return False
        
        if self.status == "COMPLETE":
            self.log("Role already complete.", "ERROR")
            return False
        
        return True
    
    def log(self, message, level=None):
        if self.logger == None: 
            print(message)
            return
        
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