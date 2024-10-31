###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Everything a Raspberry Pi Server Needs
#     Version: 1.10.22 - Updated from Code Samurai
# Description: PiNode, PiNodeController, and PiNodeCreator
#
###############################################################################

import datetime
import ipaddress
import subprocess

import requests


class PiNode:
    """
    Creates a object to easily talk to raspberry pis on the network.
    It takes in a name, The last 3 digits of the IP address, and the location
    of the pi. The location is to differetiate between the different rooms in
    the simulated reality experience.

    Public Properties:
    -port: The port number of the pi. This is hardcoded to be 12413.
    -address: The address of the pi. (Address:Port)
    -name: The name of the pi.
    -location: The location of the pi.
    -status: The CURRENT status of the pi.
    -statuses: All the statuses of the pi since the last reboot.
    -reachable: If the pi is reachable on the network.
    -changed: If the status of the pi has changed since the last get_status()

    Public Methods:
    -clear_status: Clears the status of the pi.
    -reach: Pings the pi to see if it is reachable.
    -get_status: Gets the status of the pi.
    -relay: Sends a message to the pi.
    -soft_reset: Resets the pi without powering down.
    -to_dict: Returns the information of the pi in a dictionary.
    """

    def __init__(self, name, ip_address, location=None):
        self.__name = name
        self.__ip = self.__validate_ip(ip_address)
        self.__location = location

        self.__reachable = False  # Is the Pi reachable?
        self.__status = ["OFFLINE"]
        self.__status_was = "OFFLINE"
        self.__status_time = [datetime.datetime.now()]

    def __str__(self):
        return f"PiNode: {self.name} | {self.status} | {self.location} | {self.address}"

    @property
    def port(self) -> str:
        """
        Returns the port number of the pi. This port is hardcoded to be 12413.
        This should never be changed unless you know what you're doing.
        """
        return "12413"

    @property
    def address(self) -> str:
        """
        Returns the address of the pi. This is the IP address and the port
        number.
        """
        return f"http://{self.__ip}:{self.port}"

    @property
    def name(self) -> str:
        """
        Returns the name of the pi.
        """
        return self.__name

    @property
    def location(self) -> str:
        """
        Returns the location of the pi.
        """
        return self.__location

    @property
    def status(self) -> str:
        """
        Returns the status of the pi.
        """
        return self.__status[-1]

    @property
    def status_was(self) -> str:
        """
        Returns the status of the pi before the last update.
        """
        return self.__status_was

    @property
    def statuses(self) -> list:
        """
        Returns all the statuses of the pi since the last reboot.
        """
        return self.__status

    @property
    def reachable(self) -> bool:
        """
        Returns if the pi is reachable.
        """
        return self.__reachable

    @property
    def changed(self) -> bool:
        return self.__status[-1] != self.__status_was

    def __update_status(self, status) -> None:
        """
        This updates the status of the pi. This is useful when the pi is
        resetting, and the status is not immediately available.

        This adds the status to the end of the list of the statuses so there
        is a stack of the statuses to look at.
        """
        self.__status.append(status)
        self.__status_time.append(datetime.datetime.now())
        return

    def __validate_ip(self, ipid) -> ipaddress.IPv4Address:
        """
        Check if the ip address is valid. If it is, return the ip address.
        If it is not, this is an unrecoverable error, and the program will
        exit.
        """
        try:
            ip = ipaddress.ip_address(ipid)
            return ip
        except ValueError:
            print(f"Invalid IP address: {ipid}")
            exit(1)

    def clear_status(self) -> None:
        """
        This clears the current status of the pi. This is useful when
        resetting a room.
        """
        self.__status = "OFFLINE"
        self.__reachable = False
        return

    def reach(self) -> bool:
        """
        This function pings the pi to see if it is reachable. This tests that
        that pi is simply on the network, not if it's running all the code
        it needs to run.

        ***This should only be ran if get_status fails.***

        This WILL NOT catch if the pi has failed without being cleared first,
        or if the "get_status" fails then the "reachable" will be set to False.
        """
        if self.__reachable:
            return True

        try:
            response = subprocess.run(
                ["ping", "-c", "1", self.__ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if response.returncode == 0:
                self.__reachable = True
            else:
                self.__reachable = False
        except Exception as e:
            print(f"An error occurred: {e}")
            self.__reachable = False
        return self.__reachable

    def get_status(self) -> bool:
        """
        This function gets the status of a pi. It returns the "reachable"
        value, not the status of the pi. This is meant to be used to update
        the statuses, and give a boolean to the function checking the statuses.

        The actual status needs to be pulled from the status variable.
        """
        self.__status_was = self.__status[-1].copy()
        try:
            response = requests.get(self.address + "/status", timeout=10)
            if response.status_code == 200:
                last_word = response.text.split()[-1]
                status = last_word.upper()
                self.__update_status(status)
                self.__reachable = True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.__status = "ERROR"
            self.__reachable = False

        return self.__reachable

    def soft_reset(self) -> bool:
        """
        This changes the LOCAL status of the pi to "RESETTING" and sends a
        request to the pi to reset itself. If the pi is reachable, and the
        request is successful, it will return True. If the pi is not reachable,
        or the request fails, it will return False.

        A soft reset means "software reset" the raspberry pi should not
        power down.
        """
        self.__status_was = self.__status
        self.__status = "RESETTING"
        return self.relay("reset")

    def relay(self, message) -> bool:
        """
        This sends a relay to the pi so it knows what is happening in the room.
        Each pi module decides if it's important or not, this is NOT a command
        this is purely sending a message.
        """
        try:
            response = requests.get(self.address + "/relay/" + message, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            return False

    def to_dict(self):
        """
        This function returns the information of the pi in a dictionary.
        It includes "name", "ip", "location", and "status" as keys
        and the corresponding values as strings.
        """
        info = {}
        info["name"] = self.__name
        info["ip"] = self.address
        info["location"] = self.__location
        info["status"] = self.__status[-1]
        return info
