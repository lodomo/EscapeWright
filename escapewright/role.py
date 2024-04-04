###############################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Abstract Base Class for all roles in the experience.
#     Updated: April 1st, 2024
# Description: This serves as the base class for all the roles. It helps to
#              ensure that all roles have the same structure and can be
#              easily integrated into the experience.
#
###############################################################################

# *** DO NOT CHANGE THIS FILE ***
# Derive this class with the "role_template"
# This class ensures that the role_template is implemented correctly

# List of functions to implement
# _load() - Unique load function for the role
# _logic() - Unique logic function for the role
# _stop() - Unique stop function for the role
# _bypass() - Unique bypass function for the role

# List of inherited functions
# trigger_event(event)    - Trigger an event
# update_status(status)   - Update the status of the role
# log(message, level)     - Log a message to the logger

# List of 'hidden' functions
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

import datetime
import threading


class Role:
    def __init__(self, data):
        self.__status = None  # Property exists for status
        self.__role_thread = None
        self.__triggers = self.__set_default_triggers()

    # Properties
    @property
    def status(self):
        return self.__status

    # Public Functions
    def trigger_event(self, event):
        # Event is a string. This tells the control panel what event
        # has been triggered
        if self.observer:
            self.observer.trigger(event)
            return True

        self.log("No observer set for role", "ERROR")
        return False

    # Protected Functions

    # Private Functions
    def __set_triggers(self):
        triggers = {
            "load": self.load,
            "start": self.start,
            "reset": self.reset,
            "stop": self.stop,
        }

        # Run the _set_triggers function that should get overridden
        # By the derived class (If there's unique triggers)
        return triggers

    def __add_triggers(self, triggers: dict):
        # TODO join "self.__triggers" with incoming "triggers"
        # Check if the key is a string, and the data is a ref to a function
        return True

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
        self._load()
        return True

    def _load(self):
        # This is the unique load function for the role
        # This is where the unique load logic goes
        self.log("No unique load function defined for empty role", "ERROR")
        return False

    def start(self):
        if not self.can_start():
            return False

        self.update_status("ACTIVE")
        self.log("Role Thread Started", "INFO")
        self._start()
        self.role_thread = threading.Thread(target=self.logic)
        self.role_thread.start()
        return True

    def _start(self):
        # This is the unique start function for the role
        # This is where the unique start logic goes
        self.log("No unique start function defined for empty role", "WARNING")
        return False

    def logic(self):
        self.running = True
        while self.running:
            self.u_logic()
        return

    def _logic(self):
        # This is the unique logic function for the role
        # This is where the unique logic goes
        self.log("No unique logic function defined for empty role", "ERROR")
        self.running = False  # This is to prevent an infinite loop
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

    def _stop(self):
        # This is the unique stop function for the role
        # This is where the unique stop logic goes
        self.log("No unique stop function defined for this role", "WARNING")
        return False

    def bypass(self):
        if not self.can_bypass():
            return False

        self.update_status("BYPASSED")
        self.force_join_thread()
        self._bypass()
        return True

    def _bypass(self):
        # TODO RAISE ERROR THIS HASNT BEEN IMPLEMENTED
        return

    def can_start(self):
        if self.running:
            self.log("Role Thread already running", "ERROR")
            return False

        if self.status != "READY":
            # Log "Cannot Start Role Thread from this status. Reset Required", "ERROR"
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
