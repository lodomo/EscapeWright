###############################################################################
#
# Author: Lorenzo D. Moon (Lodomo.Dev)
# Date: April 3rd 2024
# Description: This module is responsible for managing the log files of the
#              application. It provides a class that can be used to create
#              log files and write messages to them.
#
###############################################################################

import datetime
import logging
import os
import threading


class LogManager:
    def __init__(self, level=logging.INFO, auto_refresh=True):
        self.__log_file_path = self.__create_log_file()
        self.__level = level
        self.__configure_logger()
        self.__auto_refresh = auto_refresh

        logging.info("Logger initialized")

        if auto_refresh:
            self.__prep_tomorrows_logs()
        return

    def __del__(self):
        pass

    @property
    def log_file_path(self):
        return self.__log_file_path

    @property
    def auto_refresh(self):
        return self.__auto_refresh

    def __create_log_file(self, file_name=None):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")
        ewlogs_path = os.path.join(home_dir, "EWLogs")

        # Check if EWLogs exists, create if not
        if not os.path.exists(ewlogs_path):
            os.mkdir(ewlogs_path)

        # Create a folder for the current year
        current_year = str(datetime.datetime.now().year)
        current_year_path = os.path.join(ewlogs_path, current_year)
        if not os.path.exists(current_year_path):
            os.mkdir(current_year_path)

        # Create a log file for today or a specific date
        _file_name = file_name

        if _file_name is None:
            _file_name = datetime.datetime.now().strftime("%Y-%m-%d")

        log_file_name = _file_name + ".ewlog"
        log_file_path = os.path.join(current_year_path, log_file_name)

        # Check if log file exists, create if not
        if not os.path.exists(log_file_path):
            with open(log_file_path, "w") as log_file:
                log_file.write("")  # Creates an empty log file

        return log_file_path

    def __configure_logger(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        _time = "[ %(asctime)s ] "
        _level = "[ %(levelname)s ] "
        _message = "%(message)s "
        _filename = "[ %(filename)s ]"
        _format = _time + _level + _message + _filename

        logging.basicConfig(
            filename=self.__log_file_path,
            filemode="a",  # Append mode
            format=_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            level=self.__level,
        )
        return

    def __change_log_file(self, file_name=None):
        logging.info("N.F.E.T.P.")
        self.__log_file_path = self.__create_log_file(file_name)
        self.__configure_logger()
        logging.info("New File Created")

        if self.auto_refresh:
            self.__prep_tomorrows_logs()  # Reschedule the next refresh
        return

    def __prep_tomorrows_logs(self):
        # This creates a thread that waits until midnight to change the log
        # file. This is done to ensure that the log file changes at midnight
        # regardless of when the application is started
        now = datetime.datetime.now()
        today = now.date()
        tomorrow = today + datetime.timedelta(days=1)

        # This is actually at 00:00:01 of tomorrow
        midnight = datetime.datetime.combine(tomorrow, datetime.time(0, 0, 1))
        time_to_sleep = (midnight - now).total_seconds()

        # Set a timer to call change_log_file at midnight
        timer = threading.Timer(time_to_sleep, self.__change_log_file)
        timer.start()

    def override_log_file(self, file_name):
        self.__change_log_file(file_name)
        return
