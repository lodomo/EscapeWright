###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Controls the timer for the room
#     Version: 2.1 (25 OCT 2023)
# Description: Timer controls for the room.
#              Optional length parameter for the timer.
#              Key Functions: Start, Pause, Resume, Stop, Reset
#
###############################################################################
from datetime import datetime, timedelta

# Class Functions:
#   start()               - Start the timer
#   pause()               - Pause the timer
#   resume()              - Resume the timer
#   stop()                - Stop the timer
#   reset()               - Reset the timer
#   calc_time_remaining() - Calculate the time remaining
#   format_time()         - format the time for easy reading
#   get_time()            - Get the time remaining in proper format.


class Timer:
    def __init__(self, length=60):
        self.length = length  # In minutes
        self.start_time = None  # When was the timer started?
        self.end_time = None  # When will it end?
        self.paused_time = None  # When was it paused?
        self.is_paused = False  # Is it paused?
        self.is_stopped = False  # Is it stopped?

    # Start the timer
    def start(self):
        if self.start_time is not None:
            return False

        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=self.length)
        return True

    # Pause the timer
    def pause(self):
        self.paused_time = datetime.now()
        self.is_paused = True
        return

    # Resume the timer
    def resume(self):
        delta = datetime.now() - self.paused_time
        self.end_time += delta
        self.is_paused = False
        return

    # Stop the timer
    def stop(self):
        self.is_stopped = True
        return

    # Reset the timer
    def reset(self):
        self.start_time = None
        self.end_time = None
        self.paused_time = None
        self.is_paused = False
        self.is_stopped = False
        return

    # Get the difference between current time, and end time
    def calc_time_remaining(self):
        time_remaining = None

        if self.start_time is None:
            time_remaining = timedelta(minutes=self.length)
        else:
            time_remaining = self.end_time - datetime.now()
        if time_remaining.total_seconds() <= 0:
            return timedelta(seconds=0)
        return time_remaining

    # format the time for easy reading
    def format_time(self):
        remaining = self.calc_time_remaining()
        hours, remainder = divmod(remaining.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    # Get the time remaining
    def get_time(self):
        if self.is_paused:
            return "PAUSED"

        if self.is_stopped:
            return "STOPPED"

        return self.format_time()
