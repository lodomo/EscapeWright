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
# Date: 04 APR 2024
# Purpose: Transmit data to the control panel
# Description:
#
###############################################################################

import logging
import threading
import requests


class Transmitter:
    def __init__(self, data):
        self.__name = data["name"]
        self.__control_ip = data["control_ip"]
        self.__port = data["port"]

        control_url = f"http://{self.__control_ip}:{self.__port}"
        self.__trigger_url = f"{control_url}/trigger/"
        self.__status_url = f"{control_url}/update_status/"

    def __send_request(self, url):
        if self.__control_ip is None:
            logging.error("No control ip set")
            return

        try:
            requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending request to {url}: {e}")
        return

    def __threaded_request(self, url):
        threading.Thread(target=self.__send_request, args=(url,)).start()
        return "Request sent to " + url

    def trigger(self, message):
        url = f"{self.__transmit_url}{message}"
        self.__threaded_request(url)
        logging.info(f"Triggered {message}")
        return

    def update_status(self, message):
        url = f"{self.__status_url}{self.__name}/{message}"
        self.__threaded_request(url)
        logging.info(f"Updated status to {message}")
        return
