class RoomStatus():
    BOOTING = "BOOTING"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    STOPPED = "STOPPED"
    LOADING = "LOADING"


class LoadingStatus():
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"


class ConfigKeys():
    CONFIG_YAML = "./src/config.yaml"
    PI_NODES = "pi_nodes"


class Broadcasts():
    """
    These are not all inclusive, but they are common across all the rooms.
    """
    ROOM_START = "ROOM_START"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    STOP = "STOP"
    RESET = "RESET"
