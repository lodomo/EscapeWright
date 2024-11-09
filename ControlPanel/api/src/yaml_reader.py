###############################################################################
#
#      Author: Lorenzo D. Moon
#     Purpose: Everything a Raspberry Pi Server Needs
#     Version: 1.11.08
# Description: Incredibly simple yaml reader to get the config file
#
###############################################################################

import yaml
import os


def open_yaml_as_dict(yaml_file):
    try:
        with open(yaml_file, "r") as file:
            config_dict = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File not found: {yaml_file}")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    return config_dict
