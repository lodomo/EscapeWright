###############################################################################
#        ______  _____  _____          _____  ______
#       |  ____|/ ____|/ ____|   /\   |  __ \|  ____|
#       | |__  | (___ | |       /  \  | |__) | |__
#       |  __|  \___ \| |      / /\ \ |  ___/|  __|
#       | |____ ____) | |____ / ____ \| |    | |____
#       |______|_____/ \_____/_/____\_\ |____|______|_    _ _______
#                   \ \        / /  __ \|_   _/ ____| |  | |__   __|
#                    \ \  /\  / /| |__) | | || |  __| |__| |  | |
#                     \ \/  \/ / |  _  /  | || | |_ |  __  |  | |
#                      \  /\  /  | | \ \ _| || |__| | |  | |  | |
#                       \/  \/   |_|  \_\_____\_____|_|  |_|  |_|
# ------------------------------------------------------------------------------
#
#      Author: Lorenzo D. Moon (Lodomo.Dev)
#        Date: 2024-04-04
#     Purpose: Manage Log files throughout the entire system.
# Description: This class needs to be instantiated one time to manage the log
#              files for either a client server, or the control console.
#              Currently it is not customizable other than setting logs to
#              auto-refresh at midnight. This is done to ensure that the log
#              file changes at midnight regardless of when the application is
#              started. It also has the option for what logs are written, you
#              can set the level to:
#              logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
#              logging.CRITICAL
#
###############################################################################

import datetime
import logging
import os
import threading

# Log Manager Class
# Public Methods
#     override_log_file(file_name): You can set the log file name here.
# Public Properties (Immutable)
#     log_file_path: Returns the path to the current log file.
#     auto_refresh: Returns the current state of the auto-refresh property.


class LogManager:
    def __init__(self, level=logging.INFO, auto_refresh=True):
        self.__default_folder = "EWLogs"
        self.__start_day = "A new day begins."
        self.__close_log = "N.F.E.T.P."
        self.__level = level
        self.__auto_refresh = auto_refresh
        self.__log_file_path = None
        return

    def __del__(self):
        self.__log_file_path = None
        self.__level = None
        self.__auto_refresh = None
        pass

    def run(self):
        self.__log_file_path = self.__create_log_file()
        self.__configure_logger()
        logging.info("Logging service started.")

        # If auto_refresh is set, then schedule the next log to be created.
        if self.__auto_refresh:
            self.__prep_tomorrows_logs()

    def override_log_file(self, file_name):
        # This method allows the user to override the log file name
        # This is useful for when the user wants to create a log file for a
        # specific date, or for a specific event, or for testing
        self.__change_log_file(file_name)
        return

    @property
    def log_file_path(self):
        # Returns the path to the current log file
        return self.__log_file_path

    @property
    def auto_refresh(self):
        # Returns the current state of the auto-refresh property
        return self.__auto_refresh

    def __create_log_file(self, file_name=None):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")
        ewlogs_path = os.path.join(home_dir, self.__default_folder)

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
        logging.info(self.__close_log)  # Add "End Day" message
        self.__log_file_path = self.__create_log_file(file_name)
        self.__configure_logger()

        if file_name is None:
            logging.info(self.__start_day)  # Add "Start Day" message

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
        logging.info(
            f"Next log change at: {midnight}, in {time_to_sleep} seconds.")

        # Set a timer to call change_log_file at midnight
        timer = threading.Timer(time_to_sleep, self.__change_log_file)
        timer.start()
