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
