class RoomStatus():
    BOOTING = "BOOTING"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    STOPPED = "STOPPED"


class LoadingStatus():
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"


class ConfigKeys():
    CONFIG_YAML = "./src/config.yaml"
    PI_NODES = "pi_nodes"
