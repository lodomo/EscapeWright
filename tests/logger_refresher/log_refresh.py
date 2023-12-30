################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: 
#     Updated: 09 NOV 2023 
# Description: Sample pi server
#
################################################################################

# External Imports
import os                      # Used to get the path to the .ew files
import sys                     # Used to exit the program during critical errors
import importlib               # Used to import the role
import logging                 # Used to log the program
import threading               # Used to update the logger file
import time                    # Used to sleep the thread
from datetime import datetime  # Used to get the current date

# Internal Imports
from escapewright.escapiserver import EscapiServer
from escapewright.ewfunct import ew_to_dict
from escapewright.ewfunct import relative_path

def main():
    # Get the info from the server_info.ew file
    logger = set_logger()            # Set the logger, if logging is enabled
    log_thread = threading.Thread(target=update_logger_file, args=(logger,), daemon=True)
    log_thread.start()
    logger.log(logging.INFO, "LOG CREATED")

    while True:
        time.sleep(100)
    return

def set_logger():
    log_base_dir = "EW.Logs" # Base directory for the logs

    # Get the current date for the directory structure
    # YYYY/MM/DD.ewlog
    current_date = datetime.now()
    year_dir = os.path.join(log_base_dir, str(current_date.year))
    month_dir = os.path.join(year_dir, f"{current_date.month:02d}")
    # Make the file name DDHHMMSS.ewlog
    day_file = os.path.join(month_dir, f"{current_date.minute:02d}-{current_date.second:02d}-{current_date.microsecond:02d}.ewlog")

    # Ensure the directory exists
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)
    
    # Dictionary to convert the log level from a string to a logging level
    log_level = {
                     'DEBUG': logging.DEBUG,
                      'INFO': logging.INFO,
                   'WARNING': logging.WARNING,
                     'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL
                }
    
    # Configure the logging system
    logging.basicConfig(filename=day_file,  # Log file name
                        filemode='a',        # Mode to open the file, 'w' for overwrite, 'a' to append
                        level=logging.INFO,      # Log level to capture
                        format='[%(asctime)s] %(levelname)s: %(message)s',  # Log message format
                        datefmt='%m-%d %H:%M:%S')  # Date format
    logger = logging.getLogger("name")
    return logger

def seconds_until_3am():
    # Get the current date
    current_date = datetime.now()
    # Get the time until 3am
    time_until_3am = datetime(current_date.year, current_date.month, current_date.day, 3, 0, 0) - current_date
    # Convert the time to seconds
    seconds_until_3am = time_until_3am.seconds
    return seconds_until_3am

def update_logger_file(logger):
    if logger is None:
        return

    sleep_time = seconds_until_3am()
    print(f"Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)
    
    # Remove all handlers associated with the logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    log_base_dir = "EW.Logs" # Base directory for the logs
    # Get the current date for the directory structure
    # YYYY/MM/DD.ewlog
    current_date = datetime.now()
    year_dir = os.path.join(log_base_dir, str(current_date.year))
    month_dir = os.path.join(year_dir, f"{current_date.month:02d}")
    # Make the file name DDHHMMSS.ewlog
    day_file = os.path.join(month_dir, f"{current_date.minute:02d}-{current_date.second:02d}-{current_date.microsecond:02d}.ewlog")

    # Create a new file handler with the new log file name
    new_handler = logging.FileHandler(day_file)

    # Set the log format
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m-%d %H:%M:%S')
    new_handler.setFormatter(formatter)

    # Add the new handler to the logger
    logger.addHandler(new_handler)
    logger.log(logging.INFO, "LOG CREATED")

    return update_logger_file(logger)

if __name__ == "__main__":
    main()