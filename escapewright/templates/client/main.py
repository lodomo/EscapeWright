###############################################################################
#
#        ███████████ ████████    ████████████
#        ██     ██      ██       ██   ██   ██ █
#        ███████████ ██      ██  ██████████
#        ██          ██ ██     ██████ ██     ██
#        ███████████ █████    ██     ███████
#                   █        █████████████████   ████████
#                    █    █ ██   ██   ██  ██     ██   ██   ██
#                     ████  ██████   ██  ██  █████████   ██
#                      ████   ██  █   ██  ██   ████   ██   ██
#                             ██   ████████████   ██   ██
# ------------------------------------------------------------------------------
#
#      Author: Lorenzo D. Moon (Lodomo.Dev)
#        Date: 11 April 2024
#     Purpose: Sample Client Server Setup
# Description: Settings for this server are defined in "client_info.ew"
#
###############################################################################
import importlib
import logging
import sys

from escapewright import Client, FileReader, LogManager
from escapewright.utils import relative_path


def main():
    log_manager = LogManager()
    log_manager.run()
    file_reader = FileReader("client_info.ew")
    data = file_reader.to_dict()
    data["role"] = create_role(data)
    data["site_path"] = find_file_or_dir("site")
    disable_flask_log()
    client = Client(data)
    client.run()
    return


def create_role(data):
    # Check if info have a "module" key
    if "module" not in data:
        data["module"] = "escapewright"

    # Import the module from the "module" key in the info dictionary
    module = importlib.import_module(data["module"])

    # Get the class from the "class" key in the info dictionary
    # TODO SHOULD THIS BE IN A TRY BLOCK?
    ClassToInstantiate = getattr(module, data["role"])

    # Instantiate the class
    instance = ClassToInstantiate()
    return instance


def disable_flask_log():
    # Disable Flask's default logger
    flask_log = logging.getLogger("werkzeug")
    flask_log.disabled = True
    return


def find_file_or_dir(filename):
    # Load the file, and return it
    # If the file is not found, log the error and exit:
    try:
        file = relative_path(__file__, filename)
        logging.debug(f"Found {filename}")
        return file
    except FileNotFoundError as e:
        logging.critical(f"{e}")
        print(f"EW:CRITICAL: {e}")
        print("Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
