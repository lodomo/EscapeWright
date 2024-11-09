class RoomStatus:
    def __init__(self):
        self.__LOADING = "Loading"
        self.__READY = "Ready"
        self.__RUNNING = "Running"
        self.__PAUSED = "Paused"
        self.__ERROR = "Error"
        self.__STOPPED = "Stopped"

    @property
    def LOADING(self):
        return self.__LOADING

    @property
    def READY(self):
        return self.__READY

    @property
    def RUNNING(self):
        return self.__RUNNING

    @property
    def PAUSED(self):
        return self.__PAUSED

    @property
    def ERROR(self):
        return self.__ERROR

    @property
    def STOPPED(self):
        return self.__STOPPED
