################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Template for roles, which could be puzzles, maestro, or pretty
#              much anything else.
#     Updated: 24 OCT 2023
# Description: 
#              
################################################################################

from escapewright.role import Role
from gpiozero import InputDevice, OutputDevice
from time import sleep
import threading

# INHERITED MEMBERS
# observer = None
# status = None
# running = False
# Triggers:
#  "load": self.load,
# "start": self.start,
# "reset": self.reset,
#  "stop": self.stop}

class Maze(Role):
    def __init__(self, logger = None):
        super().__init__()  # Call the parent class's initializer
        self.button = InputDevice(21, pull_up=True)
        self.maglock = OutputDevice(17)
        self.logger = logger
        self.reloadable = ["COMPLETE", "BYPASSED", "STOPPED"]
        self.is_resetting = False

        # This is for triggers unique to this Role.
        # Ex: "room_start" for roles that start at the beginning of the room
        #     "door_opened" for roles that start when a door is opened
        # trigger format is { "trigger": function }
        unique_triggers = { }

        # Add to the default triggers
        self.triggers.update(unique_triggers)
        return

    def load(self):
        self.maglock.on()
        self.status = "READY"
        self.log(f"Maglock Set to {self.maglock.value}", "INFO")
        self.is_resetting = False
        return True 
    
    def start(self):
        if self.running:
            self.log("Puzzle already running", "ERROR")
            return False

        thread = threading.Thread(target=self.puzzle)
        thread.start()
        self.log("Puzzle Started", "INFO")
        self.status = "ACTIVE"
        return True 
    
    def puzzle(self):
        while self.running:
            if self.button.is_active:
                self.maglock.off()
                self.status = "COMPLETE"
                self.log("Maglock Set to {self.maglock.value}", "INFO")
                self.running = False
        
        if self.is_resetting:
            self.load()
        
        return True
    
    def reset(self):
        self.is_resetting = True

        if self.status == "READY":
            return True

        if self.status == "COMPLETE":
            return self.load()
        
        self.running = False
        return True
    
    def stop(self):
        self.running = False
        self.maglock.off()
        self.status = "STOPPED"
        self.log("FORCE STOP, MAGLOCK OFF", "ERROR")
        return True 
    
    def bypass(self):
        self.running = False
        self.maglock.off()
        self.status = "BYPASSED"
        self.log("FORCE BYPASS, MAGLOCK OFF", "INFO")
        return True 