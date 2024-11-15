###############################################################################
# Description: Role Template.
# Version: 0.1
###############################################################################

from src.role import Role
from src.enums import Statuses
import time


class HelloRole(Role):
    """
    This is a test role.
    It will just print "Hello World" every second.
    """

    def load(self):
        print("Test Role Loaded")
        self.set_status(Statuses.READY)
        pass

    def logic(self):
        while self.__status is Statuses.ACTIVE:
            print("Hello World")
            time.sleep(1)
        pass
