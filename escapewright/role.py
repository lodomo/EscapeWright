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
# u_load() - Unique load function for the role
# u_logic() - Unique logic function for the role
# u_stop() - Unique stop function for the role
# u_bypass() - Unique bypass function for the role

### List of inherited functions
# trigger_event(event)    - Trigger an event
# update_status(status)   - Update the status of the role
# log(message, level)     - Log a message to the logger

#### List of 'hidden' functions
# set_observer(observer) - Set the observer for this role
# process_message(message) - Process a message from the control panel
# load()     - Load the pi's role
# start()    - Start the pi's role
# reset()    - Reset the pi's role 
# stop()     - Stop the pi's role 
# bypass()   - Bypass the pi's current taskrole 
# can_start(status)    - Check if the role is startable
# can_bypass(status)   - Check if the role is bypassable
# join_thread()           - Join the thread

import threading
import datetime

class Role:
    def __init__(self, logger = None):
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
        self.update_status("READY")
        self.is_resetting = False
        self.u_load()
        return True 
    
    def u_load(self):
        # This is the unique load function for the role
        # This is where the unique load logic goes
        self.log("No unique load function defined for empty role", "ERROR")
        return False
    
    def start(self):
        if not self.can_start():
            return False
        
        self.update_status("ACTIVE")
        self.log("Role Thread Started", "INFO")
        self.u_start()
        self.role_thread = threading.Thread(target=self.logic)
        self.role_thread.start()
        return True
    
    def u_start(self):
        # This is the unique start function for the role
        # This is where the unique start logic goes
        self.log("No unique start function defined for empty role", "WARNING")
        return False
    
    def logic(self):
        self.running = True
        while self.running:
            self.u_logic()
        return
    
    def u_logic(self):
        # This is the unique logic function for the role
        # This is where the unique logic goes
        self.log("No unique logic function defined for empty role", "ERROR")
        self.running = False # This is to prevent an infinite loop
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
        if self.status == "STOPPED":
            self.log("Role already stopped", "WARNING")
            return False

        self.update_status("STOPPED")
        self.force_join_thread() 
        self.u_stop()
        return True
    
    def u_stop(self):
        # This is the unique stop function for the role
        # This is where the unique stop logic goes
        self.log("No unique stop function defined for this role", "WARNING")
        return False
    
    def bypass(self):
        if not self.can_bypass(): 
            return False

        self.update_status("BYPASSED")
        self.force_join_thread()
        self.u_bypass()
        return True
    
    def u_bypass(self):
        # This is the unique bypass function for the role
        # This is where the unique bypass logic goes
        self.log("No unique bypass function defined for this role", "WARNING")
        return False
    
    def can_start(self):
        if self.running:
            self.log("Role Thread already running", "ERROR")
            return False

        if self.status != "READY":
            self.log("Cannot Start Role Thread from this status. Reset Required", "ERROR")
            return False
        return True

    def can_bypass(self):
        if self.status == "BYPASSED":
            self.log("Role already bypassed", "ERROR")
            return False
        
        if self.status == "COMPLETE":
            self.log("Role already complete.", "ERROR")
            return False
        
        return True
    
    def log(self, message, level=None):
        # Log a message to the logger

        # If no logger is set, then print the message
        if self.logger == None: 
            print(message)
            return False
        
        # Set message level and log it, defaults to Info
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
        return True