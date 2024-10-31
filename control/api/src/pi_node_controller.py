import logging
import datetime

from src.pi_node import PiNode


class PiNodeController:
    """
    TODO: Add a description of the class
    """

    def __init__(self, pi_nodes: list):
        self.__pi_nodes = pi_nodes
        self.__pi_nodes_dict = {pi.name: pi for pi in self.__pi_nodes}

    @property
    def all_ready(self) -> bool:
        ready = True
        for pi in self.__pi_nodes:
            if pi.status != "READY":
                logging.info(f"{pi.name: <15} - {pi.status: <10}")
                ready = False
        return ready

    def print_all(self):
        for pi in self.__pi_nodes:
            print(pi)

    def __log_deltatime(self, time_start, message) -> None:
        """
        Logs the time taken to complete a task.
        """
        log_message = f"{
            message} - Time taken: {datetime.datetime.now() - time_start}"
        logging.info(log_message)
        return

    def get_statuses(self):
        start = datetime.datetime.now()
        for pi in self.__pi_nodes:
            if pi.get_status():
                print(f"{pi.name: <11} | {pi.status}")
            else:
                print(f"Failed to get status of {pi.name}")
                print(f"Reaching out to {pi.name} at {pi.ip}...")
                pi.reach()
            logging.info(f"{pi.name: <15} - {pi.status: <10} - {pi.status_was: <10}")

        self.__log_deltatime(start, "Refresh Statuses")

    def soft_reset(self, name):
        try:
            pi = self.__pi_nodes_dict[name]
        except KeyError:
            self.if_print(f"Could not find {name} in PiNodes")
            return None
        return pi.soft_reset()

    def full_soft_reset(self):
        start = datetime.datetime.now()
        for pi in self.__pi_nodes:
            self.if_print(f"Soft resetting {pi.name}...")
            success = pi.soft_reset()

            if success:
                logging.info(f"{pi.name: <15} - Soft Reset In Progress")
            else:
                logging.error(f"{pi.name: <15} - Failed to Soft Reset")

        self.__log_deltatime(start, "Soft Reset")

    def get_serializable_pis(self):
        """
        Returns a list of dictionaries that contain the information of the
        Raspberry Pi Servers. This is used to send the information to the
        Control Console for Javascript to use.
        """
        return [pi.to_dict() for pi in self.__pi_nodes]

    def find_by_name(self, name) -> PiNode:
        try:
            return self.__pi_nodes_dict[name]
        except KeyError:
            self.if_print(f"Could not find {name} in PiNodes")
            return None

    def relay(self, message):
        # This should probably be turned into threads.
        for pi in self.__pi_nodes:
            pi.relay(message)

    def clear_statuses(self):
        for pi in self.__pi_nodes:
            pi.clear_status()
