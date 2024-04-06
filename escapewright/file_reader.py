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
# Author: Lorenzo D. Moon (Lodomo.Dev)
# Date: April 4th 2024
# Purpose: Read in files and output different dictionaries for settings
# Description: Reads in a file and converts the data into a dictionary or a
#              list. The data types are automatically converted to the correct
#              type (int, float, boolean, or string).
#
#              For Dicts the file must be formatted as follows:
#              - Each line must be a key-value pair separated by a colon and a
#              space. Example: "key: value"
#              - Comments are allowed and must start with a hash (#) symbol.
#              - Empty lines are allowed.
#              - The key will be stored as a string.
#              - The values can be any of the following types:
#                  - Boolean: True or False
#                  - Float: 1.0
#                  - Integer: 1
#                  - Negative: -1
#                  - String: Hello, World!
#                  - None: None
#
#               For Lists:
#               - Each line will be converted to a list item.
#
###############################################################################

import logging


class FileReader:
    def __init__(self, file_name: str = None):
        self.__file_name = None
        self.load_file(file_name)
        return

    @property
    def file_name(self):
        return self.__file_name

    def load_file(self, file_name: str) -> None:
        if file_name is None:
            return

        try:
            open(file_name, "r")
        except FileNotFoundError:
            # The file must exist, this is a critical error.
            logging.error(f"File {file_name} not found.")
            raise FileNotFoundError(f"File {file_name} not found.")

        self.__file_name = file_name
        return

    def to_dict(self):
        if self.file_name is None:
            logging.error("No file loaded.")
            raise FileNotFoundError("No file loaded.")

        data = {}

        with open(self.__file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                elif line != "":
                    key, value = line.split(": ")
                    data[key] = self.__auto_type(value)

        return data

    def to_list(self):
        if self.file_name is None:
            logging.error("No file loaded.")
            raise FileNotFoundError("No file loaded.")

        data = []

        with open(self.__file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                elif line != "":
                    data.append(self.__auto_type(line))

        return data

    def __auto_type(self, value: str) -> any:
        # Formats the incoming data to the correct type
        # Converts to int, float, or boolean. Supports negative numbers.

        # Convert to int
        if value.isdigit():
            value = int(value)
        # Convert to float
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        # Convert to negative int
        elif value[0] == "-" and value[1:].isdigit():
            value = int(value)
        # Convert to negative float
        elif value[0] == "-" and value[1:].replace(".", "", 1).isdigit():
            value = float(value)
        # Convert to booleans
        elif value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.lower() == "none":
            value = None
        return value
