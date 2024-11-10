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


class RedisKeys():
    def __init__(self):
        self.__API_WORKER_ID = "APIWorkerID"
        self.__API_ROOM_STATUS = "APIRoomStatus"
        self.__API_LOAD_PERCENTAGE = "APILoadPercentage"

    @property
    def API_WORKER_ID(self):
        return self.__API_WORKER_ID

    @property
    def API_ROOM_STATUS(self):
        return self.__API_ROOM_STATUS

    @property
    def API_LOAD_PERCENTAGE(self):
        return self.__API_LOAD_PERCENTAGE


def get_unique_id(keyname: str) -> int:
    """
    Reaches out to Redis and gets a unique ID for the keyname.
    The ID is just an incremental integer.
    Once it's gotten the ID, it increments the keyname in redis.
    """
    r = redis.Redis(host="localhost", port=6379, db=0)
    lock = r.lock(f"key_lock_{keyname}", timeout=5)

    try:
        if lock.acquire(blocking=True):
            if not r.exists(keyname):
                r.set(keyname, 0)
            cur = r.get(keyname)
            r.incr(keyname)
            return int(cur)
        else:
            print("Could not acquire lock.")
            exit(1)
    finally:
        # Release the lock
        lock.release()


def update_redis_key(keyname: str, value: str) -> None:
    """
    Update a key in Redis with a new value.
    """
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.set(keyname, value)
        print(f"{keyname} set to {value}")
    except Exception as e:
        print(f"Error setting {keyname} in Redis: {e}")
    return None


def get_redis_key(keyname: str) -> str:
    """
    Get a key in Redis with a new value.
    """
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        return r.get(keyname)
    except Exception as e:
        print(f"Error getting {keyname} in Redis: {e}")
    return None
