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
    # Name of the control panel, used for the title of the page
    room_name = "Test Host"

    # Reference Files Needed
    client_file = relative_path('client_list.ew')
    site_folder_path = relative_path('site')

    # Create the client controller, and load in the data from client_file
    client_controller = EscapiClientController(client_file)

    # Print the data from the client controller to make sure you loaded what you wanted.
    client_controller.print_simple_data()

    # Create the control panel, and run it
    control_panel = ControlPanel(room_name, client_controller, site_folder_path)
    control_panel.run()
    return 

def relative_path(file_or_directory):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_or_directory)

if __name__ == "__main__":
    main()