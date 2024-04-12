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
#     Purpose: Sample (And most likely the used) Client Server
# Description:
#
###############################################################################
import importlib
import logging

from escapewright import Client, FileReader, LogManager


def main():
    log_manager = LogManager()        # Create the log manager
    log_manager.run()                 # Run the logger
    file_reader = FileReader("server_info.ew") # Load the settings file
    data = file_reader.to_dict()      # Push that to a dictionary
    data["role"] = create_role(data)  # Turn role into a role obj
    disable_flask_log()               # Flask logs are too much
    client = Client(data)             # Create the client to run
    client.run()                      # Run the client
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


if __name__ == "__main__":
    main()
