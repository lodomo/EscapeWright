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
