from enum import Enum


class EWEnum(Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Status(EWEnum):
    INIT = "INIT"
    READY = "READY"
    ACTIVE = "ACTIVE"
    COMPLETE = "COMPLETE"
    STOPPED = "STOPPED"
    RESET = "RESET"
    ERROR = "ERROR"
    BYPASSED = "BYPASSED"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ResetKey(EWEnum):
    RESET = "G3fU$1pZo9rK7wB2!qXt"
