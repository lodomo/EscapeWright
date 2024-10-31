###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Everything a Raspberry Pi Server Needs
#     Version: 0.10.22 - New from Code Samurai
# Description: Takes in a text file and parses it and returns a list
#              of pi nodes.
#
###############################################################################

from src.pi_node import PiNode


class PiNodeGenerator:
    """
    TODO
    """

    def __init__(self, pi_list_ew):
        self.pi_list_ew = pi_list_ew
        return

    def generate(self):
        return self.__parse_pi_list()

    def __parse_pi_list(self) -> list:
        """
        Parses the pi_list_ew and returns a list of PiNode objects.
        Format of pi_list_ew:
        name:ip:location\n
        """

        pi_list_ew = self.pi_list_ew
        pi_nodes = []

        # Open file and read the lines
        try:
            with open(pi_list_ew, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Critical Error: Could not find file {pi_list_ew}")
            exit(1)

        # Parse the lines
        for line in lines:
            line = line.strip()
            # If line starts with #, it is a comment, ignore it
            if line.startswith("#"):
                continue
            if line:
                pi = line.split(":")
                if len(pi) == 3:
                    name, ip, location = pi
                    pi_node = PiNode(name, ip, location)
                    pi_nodes.append(pi_node)
                else:
                    print(f"Error: Could not parse line {line})")
        return pi_nodes
