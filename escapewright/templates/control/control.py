################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Control Panel for EscapeWright Raspberry Pi Servers
#     Updated: 06 NOV 2023 
# Description: Default control panel for EscapeWright Raspberry Pi Servers.
#              Adjust the control_info.ew file to change the name of the
#              control panel, and to enable/disable logging.
#
################################################################################

# You probably shouldn't change this file unless you know what you're doing.
# Luckily you can redownload it from the GitHub repo if you mess it up.

# External Libraries
import os                      # Used to get the path to the .ew files
import sys                     # Used to exit the program during critical errors
import logging                 # Used to log the program
from datetime import datetime  # Used to get the current date
import time
import threading

# Internal Libraries
from escapewright.controlpanel import ControlPanel
from escapewright.escapiclientcontroller import EscapiClientController
from escapewright.ewfunct import ew_to_dict, relative_path

def main():
    control_info = find_file_or_dir("control_info.ew")       # Load Control Settings
    script = find_file_or_dir("script.ew")                   # Load Script
    overrides = find_file_or_dir("overrides.ew")             # Load Overrides
    crew = find_file_or_dir("cr.ew")                         # Load Crew
    info = ew_to_dict(control_info)                          # Load Info Settings

    logger = set_logger(info)                                # Set the logger, if logging is enabled
    disable_flask_log()                                      # Disable Flask's default logger

    midnight_thread = threading.Thread(target=update_logger_file, args=(logger,), daemon=True)
    midnight_thread.start()

    name = info['name']                                      # Set Control Panel Name
    column1 = info['column1']                                # Set Control Panel Column 1 Name
    column2 = info['column2']                                # Set Control Panel Column 2 Name
    clients = find_file_or_dir("client_list.ew", logger)     # Load the client list
    site_dir = find_file_or_dir("site", logger)              # Load the site folder path

    # Create the client controller and control panel
    c_ctrl = EscapiClientController(clients, logger)
    control_panel = ControlPanel(name, script, overrides, crew, column1, column2, c_ctrl, site_dir, logger)

    # Log the start of the control panel
    if logger is not None:
        logger.info(f"Started {name} Control Panel")

    control_panel.run()
    return 

def find_file_or_dir(filename, logger = None):
    # Load the file, and return it
    # If the file is not found, log the error and exit
    try:
        file = relative_path(__file__, filename)
        if logger is not None:
            logger.debug(f"Found {filename}")
        return file
    except FileNotFoundError as e:
        if logger is not None:
            logger.critical(f"{e}")
            logger.critical("Exiting...")
        print(f"EW:CRITICAL: {e}")
        print("Exiting...")
        sys.exit(1)

def set_logger(info):
    is_logging = info['logging']    # Get the logging value from the info dict
    is_logging = is_logging.lower() # Make sure it is lowercase

    # If the logging value is not true, return None
    if is_logging != 'true':
        return None

    log_base_dir = "EW.Logs" # Base directory for the logs

    # Get the current date for the directory structure
    # YYYY/MM/DD.ewlog
    current_date = datetime.now()
    year_dir = os.path.join(log_base_dir, str(current_date.year))
    month_dir = os.path.join(year_dir, f"{current_date.month:02d}")
    day_file = os.path.join(month_dir, f"{current_date.day:02d}.ewlog")

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
                        level=log_level[info['log_level']],      # Log level to capture
                        format='[%(asctime)s] %(levelname)s: %(message)s',  # Log message format
                        datefmt='%Y-%m-%d %H:%M:%S')  # Date format
    
    logger = logging.getLogger(info['name'])
    return logger

def disable_flask_log():
    # Disable Flask's default logger
    flask_log = logging.getLogger('werkzeug')
    flask_log.disabled = True
    return 

def seconds_to_midnight():
    # Get the current date
    current_date = datetime.now()
    # Get the the time until midnight
    time_to_midnight = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0) - current_date
    # Convert the time to seconds
    seconds_until_midnight = time_to_midnight.seconds
    return seconds_until_midnight 

def update_logger_file(logger):
    if logger is None:
        return
    
    while True:
        logger.log(logging.INFO, "A welcome start to a new day")
        sleep_time = seconds_to_midnight()
        time.sleep(sleep_time)
        logger.log(logging.INFO, f"N.F.E.T.P.")

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
        day_file = os.path.join(month_dir, f"{current_date.day:02d}.ewlog")

        # Create a new file handler with the new log file name
        new_handler = logging.FileHandler(day_file)

        # Set the log format
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m-%d %H:%M:%S')
        new_handler.setFormatter(formatter)

        # Add the new handler to the logger
        logger.addHandler(new_handler)



if __name__ == "__main__":
    main()