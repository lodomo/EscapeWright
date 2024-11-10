#############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Simple ID Generator through Redis
# Description: Generate a unique ID from a Redis key.
#              This is initially used to get Worker IDs for the API, but
#              can be used for any other purpose.
#
###############################################################################

import redis


class RedisKeys:
    """
    RedisKeys is a class that holds all the keys for the API to use.
    This is NOT a good class to use for other stuff. This is very specific
    to the API for the Control Panel.

    It's a good idea to not instantiate this class to a variable.
    It ensures that the keys are always the same.

    Example:
    Use RedisKeys().API_WORKER_ID to get the key for the Worker ID.
    Use RedisKeys().API_WORKER_DATA() to get the data for the Worker ID.

    It's a little convoluted to add a new key, but it's worth it to keep
    everything running smooth when a key changes slightly, or there needs
    to be a new addition.

    Some keys do not init themselves. If the key is an object, it will
    take care of itself at some point.

    Keys:
    API_WORKER_ID - The ID for the worker.
    API_ROOM_STATUS - The status of the room.
    API_LOAD_PERCENTAGE - The load percentage of the room.
    API_YAML_CONFIG - The path to the YAML config file.
    """

    def __init__(self):
        self.__API_WORKER_ID = "APIWorkerID"
        self.__API_ROOM_STATUS = "APIRoomStatus"
        self.__API_LOAD_PERCENTAGE = "APILoadPercentage"
        self.__API_YAML_CONFIG = "APIYAMLConfig"
        self.__API_ROOM_TIMER = "APIRoomTimer"
        self.__redis = redis.Redis(host="localhost", port=6379, db=0)

    def init_keys(self):
        """
        Initialize the keys to their default values.
        Very handy for starting the server.
        NOT handy for restarting the room.
        """
        self.init_redis_key(self.API_ROOM_STATUS, "LOADING")
        self.init_redis_key(self.API_LOAD_PERCENTAGE, 0)
        self.init_redis_key(self.API_YAML_CONFIG, "./src/config.yaml")
        self.init_redis_key(self.API_WORKER_ID, 0)
        # Pi's are created by gunicorn.conf.py
        # Timer is created by gunicorn.conf.py

    @property
    def API_WORKER_ID(self):
        """
        Get the key for the Worker ID.
        """
        return self.__API_WORKER_ID

    def API_WORKER_DATA(self) -> int:
        """
        Get the data for the Worker ID.
        """
        return int(self.__get_key(self.API_WORKER_ID))

    @property
    def API_ROOM_STATUS(self):
        """
        Get the key for the Room Status.
        """
        return self.__API_ROOM_STATUS

    def API_ROOM_STATUS_DATA(self) -> str:
        return self.__get_key(self.API_ROOM_STATUS)

    @property
    def API_LOAD_PERCENTAGE(self):
        return self.__API_LOAD_PERCENTAGE

    def API_LOAD_PERCENTAGE_DATA(self) -> int:
        return int(self.__get_key(self.API_LOAD_PERCENTAGE))

    @property
    def API_YAML_CONFIG(self):
        return self.__API_YAML_CONFIG

    def API_YAML_CONFIG_DATA(self) -> str:
        return self.__get_key(self.API_YAML_CONFIG)

    @property
    def API_ROOM_TIMER(self):
        return self.__API_ROOM_TIMER

    def API_ROOM_TIMER_DATA(self) -> int:
        return self.__get_key(self.API_ROOM_TIMER)

    def get_unique_id(self, keyname: str) -> int:
        """
        Reaches out to Redis and gets a unique ID for the keyname.
        The ID is just an incremental integer.
        Once it's gotten the ID, it increments the keyname in redis.
        """
        lock = self.__redis.lock(f"key_lock_{keyname}", timeout=5)

        try:
            if lock.acquire(blocking=True):
                if not self.__redis.exists(keyname):
                    self.__redis.set(keyname, 0)
                cur = self.__redis.get(keyname)
                self.__redis.incr(keyname)
                return int(cur)
            else:
                print("Could not acquire lock.")
                exit(1)
        finally:
            # Release the lock
            lock.release()

    def update_key(self, keyname: str, value: str) -> None:
        """
        Update a key in Redis with a new value.
        """
        try:
            self.__redis.set(keyname, value)
            print(f"{keyname} set to {value}")
        except Exception as e:
            print(f"Error setting {keyname} in Redis: {e}")
        return None

    def init_redis_key(self, keyname: str, value: str):
        try:
            self.__redis.set(keyname, value)
            print(f"{keyname} set to {value}")
        except Exception as e:
            print(f"Error setting {keyname} in Redis: {e}")
            exit(1)

    def __get_key(self, keyname: str) -> str:
        """
        Get a key in Redis with a new value.
        """
        try:
            value = self.__redis.get(keyname)
            return value.decode("utf-8") if value else None
        except Exception as e:
            print(f"Error getting {keyname} in Redis: {e}")
        return None
