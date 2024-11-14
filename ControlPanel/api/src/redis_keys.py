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
from enum import Enum


class RedisKeys(Enum):
    """
    This holds the main globals for the API
    There are other keys that exist out there (like the Pis)
    The Pi keys cannot be retrieved like the rest.

    ***IMPORTANT***
    No keys here are responsible for setting themselves in redis.
    """
    REDIS = redis.Redis(host="localhost", port=6379, db=0)
    GUNICORN_PID = "GUNICORN_PID"
    API_WORKER_ID = "APIWorkerID"
    API_ROOM_STATUS = "APIRoomStatus"
    API_LOAD_PERCENTAGE = "APILoadPercentage"
    API_YAML_CONFIG = "APIYAMLConfig"
    API_ROOM_TIMER = "APIRoomTimer"

    def get(self) -> str:
        string = self.value
        r = RedisKeys.REDIS.value
        return r.get(string).decode("utf-8")

    def set(self, value) -> None:
        string = self.value
        r = RedisKeys.REDIS.value
        r.set(string, value)
        return

    def get_then_increment(self):
        """
        This should only be used for the APIWorkerID, but can be used for any
        key that is a number that can be incremented.
        """
        keyname = self.value
        r = RedisKeys.REDIS.value
        lock = r.lock(f"key_lock_{keyname}", timeout=5)

        try:
            if lock.acquire(blocking=True):
                if not r.exists(keyname):
                    r.set(keyname, 0)
                cur = r.get(keyname)
                r.incr(keyname)
                return cur
            else:
                print("Could not acquire lock.")
                exit(1)
        finally:
            # Release the lock
            lock.release()
