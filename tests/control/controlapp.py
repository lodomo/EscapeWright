################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: 
#     Updated: 25 OCT 2023
# Description: Sample control server 
#
################################################################################

import os
from escapewright.controlpanel import ControlPanel
from escapewright.escapiclient import EscapiClient
from escapewright.escapiclientcontroller import EscapiClientController

def main():
    clients = []
    client_controller = EscapiClientController(clients)
    site_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
    control_panel = ControlPanel("Test Host", client_controller, site_folder_path)
    control_panel.run()
    return 

if __name__ == "__main__":
    main()