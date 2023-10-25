################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: For a Control Server to interact with a Raspberry Pi server
#     Updated: 24 OCT 2023
# Description: This class is used to store all the information about a
#              Raspberry Pi server. It is used to store the name, ip, port,
#              address, status, and reachability of the server. It also has
#              functions to reset the server, and to get the status of the
#              server.
#
################################################################################

from .escapiclient import EscapiClient as Client
from .escapiserver import EscapiServer as Server