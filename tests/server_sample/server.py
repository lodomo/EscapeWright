################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: 
#     Updated: 05 NOV 2023 
# Description: Sample pi server
#
################################################################################

import os
import sys
import importlib
import logging

from escapewright.escapiserver import EscapiServer
from escapewright.ewfunct import ew_to_dict
from escapewright.ewfunct import relative_path

def main():
    # Get the info from the server_info.ew file
    info = ew_to_dict(relative_path(__file__, 'server_info.ew'))
    site_dir = find_file_or_dir("site")              # Load the site folder path
    server = EscapiServer(info['name'], create_role(info), site_dir, info['location'], int(info['port']))
    server.start_server()
    return

def guarantee_path():
    # Find the role, and instantiate it
    # This makes sure the current folder is is the python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.append(script_dir) 

def create_role(info):
    # Import the module from the "role" key in the info dictionary
    module = importlib.import_module(info['role'])

    # Get the class from the "class" key in the info dictionary
    ClassToInstantiate = getattr(module, info['class'])

    # Instantiate the class
    instance = ClassToInstantiate()
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

if __name__ == "__main__":
    main()