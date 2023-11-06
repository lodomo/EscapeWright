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
from escapewright.escapiserver import EscapiServer
from escapewright.ewfunct import ew_to_dict

def main():
    # Get the info from the server_info.ew file
    info = ew_to_dict(relative_path('server_info.ew'))
    server = EscapiServer(info['name'], create_role(info), info['location'], int(info['port']))
    return

def relative_path(file_or_directory):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_or_directory)

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

if __name__ == "__main__":
    main()