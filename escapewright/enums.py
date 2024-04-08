from enum import Enum


class Status(Enum):
    INIT = "INIT"
    READY = "READY"
    ACTIVE = "ACTIVE"
    COMPLETE = "COMPLETE"
    STOPPED = "STOPPED"
    RESET = "RESET"
    ERROR = "ERROR"
    BYPASSED = "BYPASSED"
