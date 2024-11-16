import time

from src.redis_keys import RedisKeys


class TimerStates:
    """
    This class is used to define the states of the timer.
    """
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"


class Timer:

    def __init__(
        self,
        length: int = 60,
        redis_key: str = RedisKeys.API_ROOM_TIMER.get(),
        new_timer: bool = False,
    ):
        """
        The timer class is tricky since it needs to be able to communicate
        with any of the instances of the gunicorn server. Since this is shared
        memory it needs to log and get all it's states from redis, not from
        itself.

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


        TREAT Timer() like a global!! It's shared memory if you don't
        define a new redis_key
        """
        self.redis_key = redis_key
        self.__length = length
        self.__start_time = 0
        self.__end_time = 0
        self.__paused_time = 0
        self.__has_started = False
        self.__is_paused = False
        self.__is_stopped = False

        if new_timer:
            self.reset()
        else:
            self.load_from_redis()

    def __str__(self) -> str:
        """
        Format the data for saving to redis.
        """
        redis_format = f"{self.__length}:"
        redis_format += f"{self.__start_time}:"
        redis_format += f"{self.__end_time}:"
        redis_format += f"{self.__paused_time}:"
        redis_format += f"{self.__has_started}:"
        redis_format += f"{self.__is_paused}:"
        redis_format += f"{self.__is_stopped}"
        return redis_format

    def save_to_redis(self):
        """
        Save the timer data to the redis key
        """
        RedisKeys.API_ROOM_TIMER.set(self.__str__())
        return

    def load_from_redis(self):
        """
        Load the timer data from the redis key. This should be done
        when the timer is doing anything to change states incase it already
        did change a state.
        """
        data = RedisKeys.API_ROOM_TIMER.get()

        if data is None:
            print("No timer data found in redis.")
            return False

        data = data.split(":")
        self.__start_time = int(data[1])
        self.__end_time = int(data[2])
        self.__paused_time = int(data[3])
        self.__has_started = self.string_to_bool(data[4])
        self.__is_paused = self.string_to_bool(data[5])
        self.__is_stopped = self.string_to_bool(data[6])
        return True

    def string_to_bool(self, string: str) -> bool:
        """
        Convert a string to a boolean.
        """
        if string == "True":
            return True
        elif string == "False":
            return False
        raise ValueError("String is not a boolean.")

    @property
    def length(self) -> int:
        """
        Returns the length of the timer. This is set at the start
        of runtime and cannot be dynamically changed.
        """
        return self.__length

    @property
    def start_time(self) -> int:
        """
        Returns an ugly int start time, this is purely for debugging
        """
        self.load_from_redis()
        return self.__start_time

    @property
    def end_time(self):
        """
        Returns an ugly int end time, this is purely for debugging
        """
        self.load_from_redis()
        return self.__end_time

    @property
    def paused_time(self):
        """
        Returns an ugly int paused time, this is purely for debugging
        """
        self.load_from_redis()
        return self.__paused_time

    @property
    def has_started(self):
        """
        Check if the timer has started.
        """
        self.load_from_redis()
        return self.__has_started

    @property
    def is_paused(self):
        """
        Check if the timer is paused.
        """
        self.load_from_redis()
        return self.__is_paused

    @property
    def is_stopped(self):
        """
        Check if the timer is stopped
        """
        self.load_from_redis()
        return self.__is_stopped

    # Start the timer
    def start(self) -> bool:
        """
        Starts the timer.
        If the time is already running, raise a ValueError.
        Sets start time to now, and sets endtime based on "self.length".
        """
        self.load_from_redis()

        if self.__has_started:
            return False

        if self.__is_stopped:
            raise ValueError("Timer is stopped. Reset the timer to start.")

        self.__has_started = True
        self.__start_time = int(time.time())
        self.__end_time = int(time.time()) + (self.__length * 60)
        self.save_to_redis()
        return True

    def pause(self):
        """
        Sets a is_paused flag to True, and sets the paused_time to now.
        On resume, the time will be adjusted to account for the pause.
        Raises an error if the timer is already paused.
        """
        self.load_from_redis()
        if self.__is_paused:
            raise ValueError("Timer is already paused.")

        self.__paused_time = int(time.time())
        self.__is_paused = True
        self.save_to_redis()
        return

    def resume(self):
        """
        Resumes the timer accounting for the time paused.
        Raises an error if the timer is not paused.
        """
        self.load_from_redis()
        if not self.__is_paused:
            raise ValueError("Timer can't resume if it's not paused.")

        delta = int(time.time()) - self.__paused_time
        self.__end_time += delta
        self.__is_paused = False
        self.save_to_redis()
        return

    def stop(self):
        """
        Stops the timer, and sets the is_stopped flag to True.
        The timer can't be resumed after being stopped!
        You must reset the timer to start it again.
        """
        self.load_from_redis()
        self.__is_stopped = True
        self.__end_time = 0
        self.save_to_redis()
        return

    def reset(self) -> None:
        """
        Resets all the timer data, and allows the timer to be started again.
        Reset has NOTHING to stop it from happening.
        If you call reset, it resets.
        Always succeeds.
        """
        self.load_from_redis()
        self.__start_time = 0
        self.__end_time = 0
        self.__paused_time = 0
        self.__has_started = False
        self.__is_paused = False
        self.__is_stopped = False
        self.save_to_redis()
        return

    def get_remaining_time(self) -> str:
        """
        Get the time remaining in proper format.
        If the timer is paused, return "PAUSED".
        If the timer is stopped, return "STOPPED".
        Format is "HH:MM:SS"
        """
        self.load_from_redis()

        if self.__is_paused:
            remaining_time = self.__end_time - self.__paused_time
        else:
            remaining_time = self.__calc_time_remaining()

        return int(remaining_time)

    def get_time_formatted(self) -> str:
        time = self.get_remaining_time()
        return self.__format_time(time)

    def __calc_time_remaining(self) -> int:
        """
        Calculate the time remaining on the timer. Returns a timedelta object.
        This should be only ran internally, and not called by the user.
        """
        self.load_from_redis()
        time_remaining = None

        if not self.__has_started:
            time_remaining = self.__length * 60
        else:
            time_remaining = int(self.__end_time) - int(time.time())

        if time_remaining <= 0:
            return 0
        return time_remaining

    def __format_time(self, seconds) -> str:
        """
        Format the time in a string of "HH:MM:SS"
        """
        self.load_from_redis()
        hrs, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hrs), int(mins), int(secs))
