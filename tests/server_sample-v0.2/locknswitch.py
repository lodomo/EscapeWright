################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Template for roles, which could be puzzles, maestro, or pretty
#              much anything else.
#     Updated: 20 NOV 2023 
# Description: 
#              
################################################################################

from escapewright.role import Role
from time import sleep
from gpiozero import InputDevice, OutputDevice

# Inherited functions
# trigger_event(event) - Trigger an event 
# update_status(status) - Update the status of the role
# log(message, level) - Log a message to the logger
# join_thread() - Set "running" to False and wait till function is completed
# can_start(status)    - Check if the role is startable
# can_bypass(status)   - Check if the role is bypassable


class LockNSwitch(Role):
    def __init__(self, logger = None, switch_pin = 21, maglock_pin = 17):
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
                          "bypass": self.bypass
                          }

        ### Unique Members ###
        # trigger format is { "trigger": function }
        unique_triggers = {}
        self.triggers.update(unique_triggers)

        # Add any unique members here
        self.switch = InputDevice(switch_pin, pull_up=True)
        self.maglock = OutputDevice(maglock_pin)
        return
    
    def u_load(self):
        self.maglock.on()
        return True
    
    def u_start(self):
        # No Unique Start tasks 
        return True
    
    def u_logic(self):
        if not self.switch.is_active:
            sleep(1/60) # 60Hz Checking
            return False

        self.maglock.off()
        self.update_status("COMPLETE")
        self.log("Role Thread Complete", "INFO")
        self.running = False
        return True 
    
    def u_stop(self):
        self.maglock.off()
        return True
    
    def u_bypass(self):
        self.maglock.off()
        return True