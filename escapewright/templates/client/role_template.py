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
#     Purpose: Template for a derived Role class.
# Description: Use this template to write the scripts for future games. You can
#              copy and paste this template into a new file and rename it to
#              the name of the role you are creating. Then, fill in the
#              functions with the logic for the role.
#
#              You may add as many functions as you need inside the class.
#              The functions _load, _start, _reset, _stop, _bypass, and _logic
#              are REQUIRED. If removed from the class, the program will crash.
#              You can simple set them to "return" if you do not want to use
#              them.
#
###############################################################################

# import logging

# from .enums import Status
from escapewright import Role

# FUNCTIONS YOU MIGHT NEED FROM THE ROLE CLASS:
# --------------------------------------------
# _update_status(Status): Updates the status of the role, hands it to listeners
# _relay_trigger(str): Sends a trigger to the experience to be processed.
# _finish(): Finishes the role and sends a "complete" status to the experience.
#            -Optional, pass in a trigger string to send a trigger to the exp


class RoleTemplate(Role):
    def __init__(self):
        super().__init__()

        unique_triggers = {
            "trigger_name": self._load,
        }

        self._add_triggers(unique_triggers)

    def __str__(self): 
        return "RoleTemplate"

    def __repr__(self):
        return "RoleTemplate"

    def _load(self):
        return

    def _start(self):
        return

    def _reset(self):
        return

    def _stop(self):
        return

    def _bypass(self):
        return

    def _logic(self):
        # This function will run on a loop until the role is stopped.
        # The function will run at roughly 60hz depending on the complexity.
        # If you have anything causing a wait like "input()" or "time.sleep()"
        # Obviously, the loop will slow down.
        # It simply sleeps for 1/60th of a second between each iteration.
        self._finish()  # THIS MUST BE IN YOUR LOGIC SOMEWHERE!
        return


# Run this file to test the RoleTemplate Class without needing the whole
# experience/server setup.
if __name__ == "__main__":
    role = RoleTemplate()  # Change this to the name of your role
    role.process_message("load")
    role.process_message("start")
