################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Template for roles, which could be puzzles, maestro, or pretty
#              much anything else.
#     Updated: 24 OCT 2023
# Description: 
#              
################################################################################

from .role import Role

# INHERITED MEMBERS
# observer = None
# status = None
# running = False
# Triggers:
#  "load": self.load,
# "start": self.start,
# "reset": self.reset,
#  "stop": self.stop}

class Role_Template(Role):
    def __init__(self):
        super().__init__()  # Call the parent class's initializer

        # This is for triggers unique to this Role.
        # Ex: "room_start" for roles that start at the beginning of the room
        #     "door_opened" for roles that start when a door is opened
        # trigger format is { "trigger": function }
        unique_triggers = { }

        # Add to the default triggers
        self.triggers.update(unique_triggers())
        return
    
    def load(self):
        # Load the puzzle
        # This is time to prime the GPIO pins for whatever they're going to do
        print("No load function defined for this role")
        return False
    
    def start(self):
        # Run whatever logic here for the puzzle to be solvable
        print("No start function defined for this role")
        return False
    
    def reset(self):
        # Run whatever logic here for the puzzle to reset (even if it's being solved)
        print("No reset function defined for this role")
        return False
    
    def stop(self):
        # Run whatever logic here for the puzzle to stop
        print("No stop function defined for this role")
        return False