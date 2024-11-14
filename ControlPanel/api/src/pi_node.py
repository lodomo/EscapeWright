###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Everything a Raspberry Pi Server Needs
#     Version: 1.10.22 - Updated from Code Samurai
# Description: PiNode, PiNodeController, and PiNodeCreator
#              PiNode - The information needed to talk to a Raspberry Pi
#                       It maintains all it's information on redis.
#              PiNodeController - Controls all the PiNodes.
#              PiNodeCreator - Creates PiNodes from a file.
#
###############################################################################

import datetime
import ipaddress
import subprocess
import time

import redis
import requests


class PiNode:
    """
    Creates a object to easily talk to raspberry pis on the network.
    It takes in a name, The last 3 digits of the IP address, and the location
    of the pi. The location is to differetiate between the different rooms in
    the simulated reality experience.

    The PiNodes load themselves into Redis, or retrieve themselves from Redis.
    No other class should need to know this happened.

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

    def __init__(self, name, ip_address, location=None, force_update=False):
        self.redis_key = f"PiNode:{name}"
        self.r = redis.Redis(host="localhost", port=6379, db=0)
        self.__name = name
        self.__ip = self.__validate_ip(ip_address)
        self.__location = location
        self.__status = "OFFLINE"
        self.__status_was = "OFFLINE"
        self.__status_time = time.time()
        self.__reachable = False

        if force_update:
            self.force_save_to_redis()
        else:
            self.__init_to_redis()

    def __str__(self):
        redis_format = f"{self.name}:{self.ip}:{self.location}"
        redis_format += f":{self.status}:{self.status_was}:{self.status_time}"
        redis_format += f":{self.reachable}"
        return redis_format

    def __init_to_redis(self):
        """
        Initialize the PiNode to redis.
        If the key already exists, load the data.
        """
        data = self.r.get(self.redis_key)

        if data is None:
            self.__save_to_redis()
            return
        else:
            self.__load_from_redis()
        return

    def __save_to_redis(self):
        """
        Save the timer data to the redis key
        """
        try:
            self.r.set(self.redis_key, self.__str__())
        except Exception as e:
            print(f"Error saving to redis: {str(e)}")
            return False
        return True

    def force_save_to_redis(self):
        """
        Save the timer data to the redis key
        """
        try:
            self.r.set(self.redis_key, self.__str__())
        except Exception as e:
            print(f"Error saving to redis: {str(e)}")
            return False

    def __load_from_redis(self):
        """
        Load the PiNode from redis.
        """
        data = self.r.get(self.redis_key)

        if data is None:
            # This should be redundant, but could protect in the case
            # of a redis reset.
            self.__save_to_redis()
            return False

        data = data.decode("utf-8").split(":")
        self.__location = data[2]
        self.__status = data[3]
        self.__status_was = data[4]
        self.__status_time = int(float(data[5]))
        self.__reachable = self.string_to_bool(data[6])
        return True

    def string_to_bool(self, string: str) -> bool:
        """
        Convert a string to a boolean.
        """
        if string == "True":
            return True
        elif string == "False":
            return False
        raise ValueError("String is not a boolean.")

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
    def ip(self) -> str:
        """
        Returns the IP address of the pi.
        """
        return str(self.__ip)

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
        return self.__status

    @property
    def status_was(self) -> str:
        """
        Returns the status of the pi before the last update.
        """
        return self.__status_was

    @property
    def status_time(self) -> int:
        """
        Returns the time the status was last updated.
        """
        return self.__status_time

    @property
    def reachable(self) -> bool:
        """
        Returns if the pi is reachable.
        """
        return self.__reachable

    @property
    def changed(self) -> bool:
        return self.__status != self.__status_was

    def update_status(self, status) -> None:
        """
        Updates the status of the pi.
        """
        self.__status_was = self.__status
        self.__status = status
        self.__status_time = time.time()
        return

    def __validate_ip(self, ipid) -> str:
        """
        Check if the ip address is valid. If it is, return the ip address.
        If it is not, this is an unrecoverable error, and the program will
        exit.
        """
        try:
            ip = ipaddress.ip_address(ipid)
            return str(ip)
        except ValueError:
            print(f"Invalid IP address: {ipid}")
            exit(1)

    def clear_status(self) -> None:
        """
        This clears the current status of the pi. This is useful when
        resetting a room.
        """
        self.__load_from_redis()
        self.__status = "OFFLINE"
        self.__status_was = "OFFLINE"
        self.__status_time = int(time.time())
        self.__reachable = False
        self.__save_to_redis()
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
        self.__load_from_redis()
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
        self.__save_to_redis()
        return self.__reachable

    def get_status(self) -> bool:
        """
        This function gets the status of a pi. It returns the "reachable"
        value, not the status of the pi. This is meant to be used to update
        the statuses, and give a boolean to the function checking the statuses.

        The actual status needs to be pulled from the status variable.
        """
        self.__load_from_redis()
        self.__status_was = self.__status.copy()
        try:
            response = requests.get(self.address + "/status", timeout=10)
            if response.status_code == 200:
                last_word = response.text.split()[-1]
                status = last_word.upper()
                self.update_status(status)
                self.__reachable = True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.__status = "ERROR"
            self.__reachable = False
        self.__save_to_redis()
        return self.__reachable

    def relay(self, message) -> bool:
        """
        This sends a relay to the pi so it knows what is happening in the room.
        Each pi module decides if it's important or not, this is NOT a command
        this is purely sending a message.
        """
        '''
        try:
            response = requests.get(self.address + "/relay/" + message, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            return False
        '''
        print(f"Relay not sent to {self.name} - {self.ip} - {message}")
        print(f"This function is not implemented yet. Pis are not connected.")

    def to_dict(self):
        """
        This function returns the information of the pi in a dictionary.
        It includes "name", "ip", "location", and "status" as keys
        and the corresponding values as strings.
        """
        self.__load_from_redis()
        info = {}
        info["type"] = "PiNode"
        info["name"] = self.__name
        info["ip"] = self.address
        info["location"] = self.__location
        info["status"] = self.__status
        return info


class PiNodeController:
    """
    TODO: Add a description of the class
    """

    def __init__(self, pi_nodes_data: dict, initial=False):
        generator = PiNodeGenerator(pi_nodes_data, initial)
        self.__pi_nodes = generator.generate()
        self.__pi_nodes_dict = {pi.name: pi for pi in self.__pi_nodes}

    @property
    def all_ready(self) -> bool:
        ready = True
        for pi in self.__pi_nodes:
            if pi.status != "READY":
                ready = False
        return ready

    def reach_all(self):
        """
        Purely just checks if the pis are reachable.
        Does not check if their servers are online
        Used for testing network and not for production.
        """
        for pi in self.__pi_nodes:
            pi.reach()

    def print_all(self):
        for pi in self.__pi_nodes:
            print(pi)

    def get_statuses(self):
        start = datetime.datetime.now()
        for pi in self.__pi_nodes:
            if pi.get_status():
                print(f"{pi.name: <11} | {pi.status}")
            else:
                print(f"Failed to get status of {pi.name}")
                print(f"Reaching out to {pi.name} at {pi.ip}...")
                pi.reach()

        self.__log_deltatime(start, "Refresh Statuses")

    def soft_reset(self, name):
        pi = self.find_by_name(name)
        return pi.soft_reset()

    def reset_all(self):
        for pi in self.__pi_nodes:
            pi.soft_reset()

    def get_serializable_pis(self):
        """
        Returns a list of dictionaries that contain the information of the
        Raspberry Pi Servers. This is used to send the information to the
        Control Console for Javascript to use.
        """
        pi_dict = {}
        for pi in self.__pi_nodes:
            pi_dict[pi.name] = pi.to_dict()
        return pi_dict

    def find_by_name(self, name) -> PiNode:
        try:
            return self.__pi_nodes_dict[name]
        except KeyError:
            print(f"This should never happen, but {name} was not found.")
            return None

    def broadcast(self, message):
        for pi in self.__pi_nodes:
            pi.relay(message)
        return

    def relay(self, name, message):
        """
        Relay a message to all the pi nodes.
        """
        pi = self.find_by_name(name)
        pi.relay(message)
        return

    def clear_all_statuses(self):
        for pi in self.__pi_nodes:
            pi.clear_status()

    def update_status(self, name, status):
        pi = self.find_by_name(name)
        pi.update_status(status)
        return



class PiNodeGenerator:
    """
    Generates PiNodes from the YAML Config file.
    """

    def __init__(self, pi_node_yaml_dict, do_force_update=False):
        self.pi_dicts = pi_node_yaml_dict
        self.do_force_update = do_force_update
        return

    def generate(self):
        """
        Parses the pi_list from the YAML and returns a list of PiNode objects.
        """
        pi_nodes = []

        for pi in self.pi_dicts:
            name = pi["name"]
            ip = pi["ip"]
            location = pi["location"]
            pi_node = PiNode(name, ip, location, self.do_force_update)
            pi_nodes.append(pi_node)
        return pi_nodes
