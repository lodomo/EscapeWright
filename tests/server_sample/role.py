################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Example Puzzle Class. This is a template for creating a puzzle
#     Updated: 24 OCT 2023
# Description: 
#              
################################################################################

# *** DO NOT CHANGE THIS FILE ***
# Make a subclass of this class with the "role_template"
# This class ensures that the role_template is implemented correctly

class Role:
    def __init__(self):
        self.observer = None
        self.status = None
        self.running = False

        # trigger format is { "trigger": function }
        self.triggers = { "load": self.load,
                          "start": self.start,
                          "reset": self.reset,
                          "stop": self.stop}
        return
    
    def set_observer(self, observer):
        self.observer = observer
        return   
    
    def process_message(self, message):
        for trigger in self.triggers:
            if trigger in message:
                self.triggers[trigger]
        return
    
    def update_status(self, status):
        self.status = status
        if self.observer:
            self.observer.update_status(status)
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