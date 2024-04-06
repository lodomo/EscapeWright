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
from datetime import datetime  # Used to get the current date
import time
import threading

# Internal Imports
from escapewright.escapiserver import EscapiServer
from escapewright.ewfunct import ew_to_dict
from escapewright.ewfunct import relative_path

def main():
    # Get the info from the server_info.ew file
    server_info = find_file_or_dir("server_info.ew")
    info = ew_to_dict(server_info)

    logger = set_logger(info)            # Set the logger, if logging is enabled
    disable_flask_log()                  # Disable Flask's default logger

    midnight_thread = threading.Thread(target=update_logger_file, args=(logger,), daemon=True)
    midnight_thread.start()

    name = info['name']                  # Set Server Name
    role = create_role(info, logger)     # Set Server Role
    site_dir = find_file_or_dir("site")  # Load the site folder path
    location = info['location']          # Set Server Location
    port = int(info['port'])             # Set Server Port
    control_ip = None                    # Set Server Control IP
    if info['control_ip'] != "None":
        control_ip = info['control_ip']
    
    ip = info['ip']                      # Set Server IP

    # Create the server
    server = EscapiServer(name, ip, role, site_dir, logger, location, control_ip, port)

    # Start of the server
    server.run()
    return

def guarantee_path():
    # Find the role, and instantiate it
    # This makes sure the current folder is is the python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.append(script_dir) 

def create_role(info, logger = None):
    # Import the module from the "role" key in the info dictionary
    module = importlib.import_module(info['role'])

    # Get the class from the "class" key in the info dictionary
    ClassToInstantiate = getattr(module, info['class'])

    # Instantiate the class
    instance = ClassToInstantiate(logger)
    return instance

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
                        datefmt='%m-%d %H:%M:%S')  # Date format
    
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
    return seconds_until_midnight + 2 # Add 2 seconds to make sure it is after midnight

def update_logger_file(logger):
    if logger is None:
        return
    
    while True:
        sleep_time = seconds_to_midnight()
        logger.debug(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
        logger.log(logging.INFO, "Updating log file. N.F.E.T.P.")

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
        day_file = os.path.join(month_dir, f"{current_date.day:02d}-{current_date.second:02d}.ewlog")

        # Create a new file handler with the new log file name
        new_handler = logging.FileHandler(day_file)

        # Set the log format
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m-%d %H:%M:%S')
        new_handler.setFormatter(formatter)

        # Add the new handler to the logger
        logger.addHandler(new_handler)

if __name__ == "__main__":
    main()