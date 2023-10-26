################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Example Puzzle Class. This is a template for creating a puzzle
#     Updated: 24 OCT 2023
# Description: 
#              
################################################################################

class Puzzle:
    def __init__(self):
        self.observer = None
        self.status = None
        self.triggers = { 
                            #"trigger" : self.function()
                        }
        self.running = False
        
        # Add devices here such as GPIO pins needed, etc.
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
        return
    
    def start(self):
        # Run whatever logic here for the puzzle to be solvable
        return
    
    def reset(self):
        # Run whatever logic here for the puzzle to reset (even if it's being solved)
        return