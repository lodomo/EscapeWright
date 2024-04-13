###############################################################################
#
#        ███████████ ████████    ████████████
#        ██     ██      ██       ██   ██   ██ █
#        ███████████ ██      ██  ██████████
#        ██          ██ ██     ██████ ██     ██
#        ███████████ █████    ██     ███████
#                   █        █████████████████   ████████
#                    █    █ ██   ██   ██  ██     ██   ██   ██
#                     ████  ██████   ██  ██  █████████   ██
#                      ████   ██  █   ██  ██   ████   ██   ██
#                             ██   ████████████   ██   ██
# -----------------------------------------------------------------------------
#
#      Author: Lorenzo D. Moon (Lodomo.Dev)
#        Date:
#     Purpose: Abstract Base Class for all roles in the experience.
# Description: This serves as the base class for all the roles. It helps to
#              ensure that all roles have the same structure and can be
#              easily integrated into the experience.
#
###############################################################################

import logging
import threading
import time

from .enums import Status

# *** DO NOT CHANGE THIS FILE ***
# Derive this class with the "role_template"
# This class ensures that the role_template is implemented correctly

#  Data Members:
#   Private:
#       status (str): The current status of the role
#       role_thread (threading.Thread): The thread that the role runs on
#       triggers (dict): The triggers that the role can respond to
#       trigger_listeners (list): Outside that listen for sending triggers
#       status_listeners (list): Outside that listen for status updates
#       running (bool): Whether the role is running or not
#
#   Public:
#       status (property): The current status of the role
#       running (property): Whether the role is running or not
#
#  Methods:
#   Private: (All Private methods have __ prefix)
#       default_triggers(): Returns the default triggers for the role
#       force_join_thread(): Forces the role thread to join and stop
#       relay_status(status): Tells the listeners to relay a status
#       load(): The load trigger function
#       logic(): Keep a logic loop running ran as a thread from "start"
#       start(): The start trigger function
#       reset(): The reset trigger function
#       stop(): The stop trigger function
#       bypass(): The bypass trigger function
#       can_reset(): Checks if the role can be reset
#       can_start(): Checks if the role can be started
#       can_bypass(): Checks if the role can be bypassed
#   Protected:  ( _ prefix)
#       relay_trigger(event): Tells the listeners to relay a trigger
#       add_triggers(triggers): Adds triggers to the role from derived class
#       update_status(status): Updates the status of the role
#
#       (For the derived class to implement)
#       load(): The load function for the role
#       logic(): The main logic function for the role
#       start(): The start function for the role
#       logic(): The main logic function for the role
#       reset(): The reset function for the role
#       stop(): The stop function for the role
#       bypass(): The bypass function for the role
#   Public: (For the client to use) (No prefix)
#       sub_to_triggers(listener_function):
#           Functions can subscribe to know when a trigger should be sent
#           to the control panel. But it's not the role's responsibility.
#       sub_to_status(listener_function):
#           Functions can subscribe to know when the status changes
#       process_message(message): Match functions to triggers and run them


class Role:
    # Data Members
    def __init__(self):
        self.__status = Status.INIT.value
        self.__role_thread = None
        self.__triggers = self.__default_triggers()
        self.__trigger_listeners = None
        self.__status_listeners = None
        self.__running = False

    # Properties
    @property
    def status(self):
        return self.__status

    @property
    def running(self):
        return self.__running

    # Private Methods
    def __default_triggers(self):
        triggers = {
            "load": self.__load,
            "start": self.__start,
            "reset": self.__reset,
            "stop": self.__stop,
            "bypass": self.__bypass,
        }
        return triggers

    def __force_join_thread(self):
        if self.__running:
            self.__running = False
            print("Reset in Progress. If you see this message, Press Enter")
            if self.__role_thread:
                self.__role_thread.join()
                logging.info("Role Thread Joined")
            return True
        return False

    def __relay_status(self, status: Status) -> int:
        if self.__status_listeners is None:
            return 0

        for listener in self.__status_listeners:
            listener(status)

        return len(self.__status_listeners)

    def load(self):
        return self.__load()

    def __load(self):
        if not self.__can_load():
            return False

        # Load the puzzle
        self._load()  # This should be a derived class function
        self._update_status(Status.READY)
        return True

    def __logic(self):
        self.__running = True
        while self.running:
            self._logic()
            time.sleep(1 / 60)  # 60Hz
        return

    def __start(self):
        if not self.__can_start():
            return False

        self._start()  # Run the derived class start function
        self.__role_thread = threading.Thread(target=self.__logic)
        self._update_status(Status.ACTIVE)
        self.__role_thread.start()
        return True

    def __reset(self):
        self._update_status(Status.RESET)
        if not self.__can_reset():
            return False
        
        self.__running = False
        self._reset()  # Run the derived class reset function
        self.__load()
        return True

    def __stop(self):
        self.__force_join_thread()
        self._stop()  # Run the derived class stop function
        self._update_status(Status.STOPPED)
        return True

    def __bypass(self):
        if not self.__can_bypass():
            return False

        self._update_status(Status.BYPASSED)
        self._bypass()  # Run the derived class bypass function
        # Derived function to handle closing the thread, and updating status
        # This is incase a role has multiple bypasses
        return True

    def __can_load(self):
        if self.running:
            logging.error("Role Thread already running")
            return False
        return True

    def __can_start(self):
        if self.running:
            logging.error("Role Thread already running")
            return False

        if self.status != Status.READY:
            logging.error(
                "Cannot Start Role Thread from this status. Reset Required")
            return False
        return True

    def __can_reset(self):
        logging.debug("Reset Requested")
        return True

    def __can_bypass(self):

        if self.status == Status.COMPLETE:
            return False
        return True

    # Protected Methods
    def _relay_trigger(self, event: str):
        if self.__trigger_listeners is None:
            return 0

        for listener in self.__trigger_listeners:
            listener(event)
        return len(self.__trigger_listeners)

    def _add_triggers(self, triggers: dict):
        if not isinstance(triggers, dict):
            raise TypeError("Triggers must be a dictionary")
        # self._update_status(Status.BYPASSED) The derived bypass function handles this

        # Make sure every key is a string, and every value is a function
        for key in triggers:
            if not isinstance(key, str):
                raise TypeError("Trigger keys must be strings")
            if not callable(triggers[key]):
                raise TypeError("Trigger values must be functions")

        self.__triggers.update(triggers)
        return

    def _update_status(self, status: Status) -> str:
        # Update the status of the role.
        # Send it to any listeners that are subscribed
        self.__status = status
        logging.info(f"Status Updated: {self.status}")
        self.__relay_status(self.status)
        return self.status

    def _load(self):
        raise NotImplementedError(
            "Load function not implemented by derived class")

    def _logic(self):
        raise NotImplementedError(
            "Logic function not implemented by derived class")

    def _start(self):
        raise NotImplementedError(
            "Start function not implemented by derived class")

    def _stop(self):
        raise NotImplementedError(
            "Stop function not implemented by derived class")

    def _bypass(self):
        raise NotImplementedError(
            "Bypass function not implemented by derived class")

    def _reset(self):
        raise NotImplementedError(
            "Reset function not implemented by derived class")

    def _finish(self, event: str = None):
        self.__running = False
        self._update_status(Status.COMPLETE)
        if event is not None:
            self._relay_trigger(event)
        self.__role_thread = None
        return

    # Public Methods
    def sub_to_triggers(self, listener_function):
        if self.__trigger_listeners is None:
            self.__trigger_listeners = []

        self.__trigger_listeners.append(listener_function)
        return

    def sub_to_status(self, listener_function):
        if self.__status_listeners is None:
            self.__status_listeners = []

        self.__status_listeners.append(listener_function)
        return

    def process_message(self, message) -> bool:
        # Get sent a message and check if it matches one of the triggers
        trigger_activated = False
        for trigger in self.__triggers:
            if trigger in message:
                self.__triggers[trigger]()
                trigger_activated = True
        return trigger_activated
