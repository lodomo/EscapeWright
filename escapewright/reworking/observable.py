###############################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Abstract Base Class for all observable scripts
#     Updated: April 3rd, 2024
# Description: This serves as a base class for any class that needs an observer
#
###############################################################################


class Observable:
    def __init__(self):
        self.__observers = []  # List of observers

    def __del__(self):
        self.__observers.clear()
        self.__observers = None

    def add_observer(self, observer):
        if not isinstance(observer, Observer):
            raise ValueError("Observer must be an instance of Observer")

        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass  # If the observer is not in the list, do nothing

    def _trigger(self, event):
        for observer in self.__observers:
            if observer is not None:
                observer.notify(self)

    def _status(self, name, status):
        for observer in self.__observers:
            if observer is not None:
                observer.status_update(self, name, status)


class Observer:
    pass
