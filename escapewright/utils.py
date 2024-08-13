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
# Date: 05 April 2024
# Purpose: Utility functions for escape wright that didn't merit their own
#          class/module.
# Description: This file contains utility functions that are used throughout
#              the EscapeWright package. These functions are not specific to
#              any one class or module, and are used in multiple places.
#
#              Functions:
#              is_valid_ip(ip: str) -> bool
#
#
###############################################################################

import ipaddress
import os

# from pynput.keyboard import Key, Controller

# keyboard = Controller()


def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)  # Check if it's a valid IPv4 address
        return True
    except ipaddress.AddressValueError:
        try:
            ipaddress.IPv6Address(ip)  # Check if it's a valid IPv6 address
            return True
        except ipaddress.AddressValueError:
            return False


def relative_path(script, file_or_directory):
    # Return the path to a file or directory relative to the script
    # script should be __file__
    # Generate the absolute path
    abs_path = os.path.join(os.path.dirname(
        os.path.abspath(script)), file_or_directory)

    # Check if the path exists
    if os.path.exists(abs_path):
        return abs_path
    else:
        raise FileNotFoundError(f"The path {abs_path} does not exist.")


# [def simulate_input(text: str):
# TESTING NEEDS TO HAPPEN FOR THIS FUNCTION
#   keyboard = Controller()
#   keyboard.type(text)
#   keyboard.press(Key.enter)
#   return
