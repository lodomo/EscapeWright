################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: 
#     Updated: 25 OCT 2023
# Description: Sample control server 
#
################################################################################

from escapewright.controlpanel import ControlPanel
from escapewright.escapiclient import EscapiClient
from escapewright.escapiclientcontroller import EscapiClientController

def main():
    clients = []
    client_controller = EscapiClientController(clients)
    control_panel = ControlPanel("Test Host", client_controller)
    control_panel.run()
    return 

if __name__ == "__main__":
    main()