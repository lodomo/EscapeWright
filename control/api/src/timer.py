###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Controls the timer for the room
#     Version: 2.2 Updated 10-31-2024
# Description: Timer controls for the room.
#              Optional length parameter for the timer.
#              Key Functions: Start, Pause, Resume, Stop, Reset, Get Time.
#
###############################################################################
from datetime import datetime, timedelta


class Timer:
    def __init__(self, length: int = 60):
        """
        Keep track of the room time for the Game Guide.
        Length - The length of the timer in minutes, defaults to 60 minutes.

        Public Properties:
        length      - The length of the timer.
        start_time  - Time the timer started. Returns None if not started.
        end_time    - The time the timer will end.
        paused_time - The time the timer was paused.
        is_paused   - If the timer is paused. (Recoverable)
        is_stopped  - If the timer is stopped. (Not Recoverable)

        Public Functions:
        start()        - Start the timer.
        pause()        - Pause the timer.
        resume()       - Resume the timer.
        stop()         - Stop the timer.
        reset()        - Reset the timer, clears all data.
        get_time()     - String in HH:MM:SS format, or PAUSED/STOPPED.

        Private Functions:
        calc_time_remaining() - Calculate the time remaining.
        format_time() - Format the time for easy reading.
        """
        self.__length = length
        self.__start_time = None
        self.__end_time = None
        self.__paused_time = None
        self.__is_paused = False
        self.__is_stopped = False

    @property
    def length(self):
        return self.__length

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def paused_time(self):
        return self.__paused_time

    @property
    def is_paused(self):
        return self.__is_paused

    @property
    def is_stopped(self):
        return self.__is_stopped

    # Start the timer
    def start(self) -> datetime:
        """
        Starts the timer.
        If the time is already running, raise a ValueError.
        Sets start time to now, and sets endtime based on "self.length".
        """
        if self.__start_time is not None:
            raise ValueError("Timer is already running.")

        if self.__is_stopped:
            raise ValueError("Timer is stopped. Reset the timer to start.")

        self.__start_time = datetime.now()
        self.__end_time = self.__start_time + timedelta(minutes=self.__length)
        return self.start_time

    def pause(self):
        """
        Sets a is_paused flag to True, and sets the paused_time to now.
        On resume, the time will be adjusted to account for the pause.
        Raises an error if the timer is already paused.
        """
        if self.__is_paused:
            raise ValueError("Timer is already paused.")

        self.__paused_time = datetime.now()
        self.__is_paused = True
        return

    def resume(self):
        """
        Resumes the timer accounting for the time paused.
        Raises an error if the timer is not paused.
        """
        if not self.__is_paused:
            raise ValueError("Timer can't resume if it's not paused.")

        delta = datetime.now() - self.__paused_time
        self.__end_time += delta
        self.__is_paused = False
        return

    def stop(self):
        """
        Stops the timer, and sets the is_stopped flag to True.
        The timer can't be resumed after being stopped!
        You must reset the timer to start it again.
        """
        self.__is_stopped = True
        return

    def reset(self) -> None:
        """
        Resets all the timer data, and allows the timer to be started again.
        Reset has NOTHING to stop it from happening.
        If you call reset, it resets.
        Always succeeds.
        """
        self.__start_time = None
        self.__end_time = None
        self.__paused_time = None
        self.__is_paused = False
        self.__is_stopped = False
        return

    def get_time(self) -> str:
        """
        Get the time remaining in proper format.
        If the timer is paused, return "PAUSED".
        If the timer is stopped, return "STOPPED".
        Format is "HH:MM:SS"
        """
        if self.__is_paused:
            return "PAUSED"

        if self.__is_stopped:
            return "STOPPED"

        return self.__format_time()

    def __calc_time_remaining(self) -> timedelta:
        """
        Calculate the time remaining on the timer. Returns a timedelta object.
        This should be only ran internally, and not called by the user.
        """
        time_remaining = None

        if self.__start_time is None:
            time_remaining = timedelta(minutes=self.__length)
        else:
            time_remaining = self.__end_time - datetime.now()
        if time_remaining.total_seconds() <= 0:
            return timedelta(seconds=0)
        return time_remaining

    def __format_time(self) -> str:
        """
        Format the time in a string of "HH:MM:SS"
        """
        remaining = self.__calc_time_remaining()
        hrs, remainder = divmod(remaining.total_seconds(), 3600)
        mins, secs = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hrs), int(mins), int(secs))
