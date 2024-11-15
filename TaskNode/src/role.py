###############################################################################
# Description: Role Template.
# Version: 0.1
###############################################################################

import threading
from abc import ABC, abstractmethod

from src.enums import Broadcasts, Statuses
from src.transmitter import Transmitter


class Role(ABC):
    """
    This is the Role Template.
    This is the base class for all roles.

    Things to note:
    - status : Status of the role
    - status_was : The Previous status of the role
    - triggers : The triggers that affect the role.
        - Default Triggers:
            - start  : triggers the logic() to start running
            - stop   : requests the logic stop running.
                      This will raise an exception if it does not stop in 1 second.
            - pause  : This is up to you to implement
            - resume : This is up to you to implement
    - Members to implement.
      - load() - Prepare the GPIO pins and screens for BEFORE "start"
      - logic() - Run the room logic. It is up to you to keep this alive in a loop.
    """

    def __init__(self, config: dict = None):
        self.__status = Statuses.INIT
        self.__status_was = Statuses.INIT
        self.__role_thread = threading.Thread(target=self.logic)
        self.relays = []
        self.triggers = {
            Broadcasts.START: self.start,
            Broadcasts.STOP: self.stop,
            Broadcasts.PAUSE: self.pause,
            Broadcasts.RESUME: self.resume,
        }

        if config:
            self.transmitter = Transmitter(config)
            print(self.transmitter.info())
        else:
            self.transmitter = None
            print("No config provided, this role will not be able to transmit")
        pass

    @property
    def status(self):
        return self.__status

    @abstractmethod
    def load(self):
        """
        This should be called when the role is first loaded.
        It should initialize the role and set the status to READY.
        Some roles (like games) need to load data before they start.
        This should also initialize the GPIO pins and screens.
        """
        pass

    @abstractmethod
    def logic(self):
        pass

    def pause(self):
        self.set_status(Statuses.PAUSED)
        pass

    def resume(self):
        status_was = self.__status_was.copy()
        self.set_status(status_was)
        pass

    def set_status(self, status):
        self.__status_was = self.__status
        self.__status = status

        if self.transmitter:
            self.transmitter.update_status(status)
        pass

    def send_trigger(self, trigger):
        """
        This is called when the Role wants to ACTIVATE a trigger
        This is NOT to respond to a trigger
        """
        if self.transmitter:
            self.transmitter.trigger(trigger)
        return

    def relay(self, trigger) -> bool:
        """
        This is called when the Role receives a trigger
        If the trigger is a standard callable function, call it.
        Otherwise append it to the relays for the "logic" to handle.
        """
        if trigger in self.triggers:
            if trigger is not Broadcasts.START:
                self.relays.append(self.triggers[trigger])

            # if it's a function also call it.
            if callable(self.triggers[trigger]):
                self.triggers[trigger]()
            return True
        return False

    def start(self):
        """
        This should make a thread of the "logic" function
        Sometimes you just call "start" when the role is ready.
        This can happen inside the "load" function in derived classes
        """
        self.set_status(Statuses.ACTIVE)
        self.__role_thread.start()
        pass

    def stop(self):
        """
        Sets the status to stopped.
        Logic is responsible for checking if it's stopped.
        Some logic has blockers (like "input()") and cannot be stopped.
        If it cannot be stopped the caller should be responsible for handling.
        (the API)
        """
        self.set_status(Statuses.STOPPED)
        self.__role_thread.join(timeout=1)

        if self.__role_thread.is_alive():
            raise TimeoutError("Role Thread did not stop in time")
        return


class RoleTemplate(Role):
    """
    Base your new roles off this template
    Each Role Class should be unique and have it's own triggers.
    """

    def __init__(self, config: dict = None):
        """
        This is where you can add new triggers.
        self.triggers["new_trigger"] = self.function_to_call
        """
        super().__init__(config)
        pass

    def load(self):
        """
        This should be called when the role is first loaded.
        It should initialize GPIO Pins, Screens, and other hardware.
        It should end with setting the status to READY.
        """
        self.set_status(Statuses.READY)
        pass

    def logic(self):
        """
        Logic is trickier, it should be in a loop that checks the status
        If it's ACTIVE, it should run the logic, if it's not it should wait.

        Sometimes it should exit this loop.
        Sometimes it should sleep if paused.

        When the role gets a trigger, it should handle it by popping the trigger
        off the self.relays stack.
        """
        while self.__status is Statuses.ACTIVE:
            print("Hello World")
        pass
