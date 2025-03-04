###############################################################################
# Description: Transmits messages to the control panel
# Version: 0.1
###############################################################################

import threading

import requests


class Transmitter:
    def __init__(self, data):
        self.__name = data["name"]
        self.__activated = False
        self.__control_ip = None
        self.__port = None
        self.__trigger_url = None
        self.__status_url = None

        if "control_panel" in data:
            self.__activated = True
            self.__control_ip = data["control_panel"]["ip"]
            self.__port = data["control_panel"]["port"]
            control_url = f"http://{self.__control_ip}:{self.__port}"
            self.__trigger_url = f"{control_url}/trigger"
            self.__status_url = f"{control_url}/update_status"
        else:
            print(
                "No control panel data provided, this role will not be able to transmit"
            )

    def info(self):
        return {
            "name": self.__name,
            "control_ip": self.__control_ip,
            "port": self.__port,
            "trigger_url": self.__trigger_url,
            "status_url": self.__status_url,
        }

    def __send_request(self, url):
        if not self.__activated:
            return "Transmitter not activated"

        attempts = 10
        while attempts > 0:
            try:
                requests.get(url, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"Error sending request to {url}: {e}")
        return

    def __threaded_request(self, url):
        threading.Thread(target=self.__send_request, args=(url,)).start()
        return "Request sent to " + url

    def trigger(self, message):
        url = f"{self.__transmit_url}/{message}"
        self.__threaded_request(url)
        return

    def update_status(self, message):
        url = f"{self.__status_url}/{self.__name}/{message}"
        self.__threaded_request(url)
        return
