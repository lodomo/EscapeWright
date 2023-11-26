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
from time import sleep

# Inherited functions
# trigger_event(event) - Trigger an event 
# update_status(status) - Update the status of the role
# log(message, level) - Log a message to the logger
# join_thread() - Set "running" to False and wait till function is completed
# can_start(status)    - Check if the role is startable
# can_reset(status)   - Check if the role is resettable
# can_bypass(status)   - Check if the role is bypassable

class RoleTemplate(Role):
    def __init__(self, logger = None):
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

    def u_load(self):
        # Add any unique load functions here
        return
    
    def u_start(self):
        # Add any unique start functions here
        # Happens before the logic starts
        return
    
    def u_logic(self):
        # Add any unique logic functions here
        # This logic will run infinitely until "self.running" is set to false
        # You are in charge of setting "self.running" to false
        # You are in charge of setting the Hz, otherwise it will run
        # as fast as the processor will allow
        # If you do not want a loop, create a function called "logic" and it
        # will override the default logic function
        return
    
    def u_stop(self):
        # Add any unique stop functions here
        return
    
    def u_bypass(self):
        # Add any unique bypass functions here
        return