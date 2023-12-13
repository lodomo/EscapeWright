################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Create and setup any Escape Wright server. 
#     Updated: December 13th, 2023 
# Description: Wizard to create an Escape Wright server. 
#              
################################################################################

import os
import shutil
from importlib import util
import subprocess

from escapewright.ewfunct import relative_path

CONTROL = "control"
SERVER = "server"

def main():
    welcome()

    # Go to the correct menu
    if check_if(CONTROL):
        print("Control Panel Menu")
        control_panel_menu()
    elif check_if(SERVER):
        print("Server Menu")
    else:
        setup_menu()

    exit()
    return

def welcome():
    # Print the welcome message
    print(" ______  _____  _____          _____  ______    ")
    print("|  ____|/ ____|/ ____|   /\   |  __ \|  ____|   ")
    print("| |__  | (___ | |       /  \  | |__) | |__      ")
    print("|  __|  \___ \| |      / /\ \ |  ___/|  __|     ")
    print("| |____ ____) | |____ / ____ \| |    | |____    ")
    print("|______|_____/_\_____/_/__ _\_\_|_   |______|__ ")
    print("                \ \        / /  __ \|_   _/ ____| |  | |__   __|")
    print("                 \ \  /\  / /| |__) | | || |  __| |__| |  | |   ")
    print("                  \ \/  \/ / |  _  /  | || | |_ |  __  |  | |   ")
    print("                   \  /\  /  | | \ \ _| || |__| | |  | |  | |   ")
    print("                    \/  \/   |_|  \_\_____\_____|_|  |_|  |_| ")
    print("      Welcome to the Escape Wright Server Setup Wizard!")
    return

def check_if(type):
    # Check if a folder exists
    try:
        relative_path(__file__, type)
        print(f"A {type} already exists. Let's head to the {type} menu.")
        return True 
    except FileNotFoundError:
        return False

def setup_menu():
    EXIT = 0
    # Setup menu to create a control or server
    print("Menu:")
    print("1. Create a new Control Panel")
    print("2. Create a new Escape Wright puzzle server")
    print("3. Exit")
    user_input = str(input("Select an option: "))

    menu_cases = {
        "1" : create_control,
        "2" : create_server,
    }

    if user_input == str(EXIT):
        return False

    if user_input in menu_cases:
        menu_cases[user_input]()
    return 

def control_panel_menu():
    # Menu to edit a control panel server
    EXIT = 0
    print("Menu:")
    print("1. Edit an existing control panel server")
    print("2. Delete an existing control panel server")
    print("0. Exit")
    user_input = str(input("Select an option: "))

    menu_cases = {
        "1" : edit,
        "2" : delete
    }

    if user_input == str(EXIT):
        return False

    if user_input in menu_cases:
        menu_cases[user_input]()
    else:
        print("Invalid input.")

    if again():
        if check_if(CONTROL):
            control_panel_menu()
        else:
            setup_menu()

    return

def again():
    # Ask the user if they want to do something else
    user_input = input("Would you like to do something else? (y/n): ")
    user_input = user_input.lower()

    if user_input == "y":
        print() # New line
        return True
    elif user_input == "n":
        print() # New line
        return False
    else:
        print("Invalid input. Returning to menu.\n")

    return True

def create_control():
    if check_if_exists(CONTROL): return
    if not clone_directory(CONTROL): return
    create_control_info()
    create_client_list()

    # Todo add in creating the client list 

    if again():
        control_panel_menu()

    return

def create_server():
    if check_if_exists(SERVER): return
    if not clone_directory(SERVER): return
    create_server_info()
    return

def check_if_exists(folder):
    try:
        relative_path(__file__, folder)
        print("ERROR: A control panel server already exists.")
        print("Choose 'Edit an existing control panel server' from the menu to edit the server.")
        return True
    except FileNotFoundError:
        return False 

def clone_directory(folder):
    # Clone the 'templates/folder' directory to the current directory

    # Find the 'escapewright' module directory
    module_spec = util.find_spec("escapewright")
    if module_spec is not None and module_spec.origin is not None:
        escapewright_path = os.path.dirname(module_spec.origin)
        templates_control_path = os.path.join(escapewright_path, 'templates', folder)
        
        # Check if the 'templates/control' directory exists
        if os.path.isdir(templates_control_path):
            # Clone 'templates/control' to the current directory
            destination_path = os.path.join(os.getcwd(), folder)
            shutil.copytree(templates_control_path, destination_path)
            print(f"{folder} template has been cloned to the current directory: {destination_path}")
            return True
        else:
            print(f"The '{folder} template' directory does not exist in the 'escapewright' library at {templates_control_path}")
            print(f"Reinstall the escapewright library.")
            return False
    else:
        print("The 'escapewright' module is not installed or could not be found.")
    return False

def create_control_info():
    # Create the control_info.ew file
    name = input("Enter the name of the server: ")
    logging = input("Enable logging? (y/n): ")
    if logging == "y":
        logging = True
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        print("Log levels: ", end="")
        for level in log_levels:
            print(f"{level} ", end="")
        print()
        log_level = input("Enter the logging level (or press enter for default): ")
        log_level = log_level.upper()
        if log_level not in log_levels:
            if log_level != "":
                print("Invalid logging level.")
            print("Defaulting to 'INFO'")
            log_level = "INFO"
    else:
        logging = False
        log_level = "NONE"
    
    server_info = {
        "name" : name,
        "logging" : logging,
        "log_level" : log_level
    }

    control_info_file = relative_path(__file__, "control/control_info.ew")

    with open(control_info_file, "w") as f:
        for key in server_info:
            f.write(f"{key}: {server_info[key]}\n")
        print("Server info file created successfully.")
    
    print("Server settings are as follows:")
    print(f"Name: {name}")
    print(f"Logging: {logging}")
    print(f"Log level: {log_level}")

    return True

def create_client():
    # name: sample_client
    # ip_address: 0.0.0.0
    # port: 12413 
    # location: sample_location 
    name = input("Enter the name of the client: ")
    ip_address = input("Enter the IP address of the client: ")
    port = input("Enter the port of the client (Leave blank for default): ")
    location = input("Enter the location of the client: ")

    if port == "":
        port = 12413
    
    client = {
        "name" : name,
        "ip_address" : ip_address,
        "port" : port,
        "location" : location
    }

    return client

def create_client_list():
    print("\nEnter the information for each client.")
    client_list = []

    client_list.append(create_client())

    while True:
        if input("Add another client? (y/n): ") == "y":
            client_list.append(create_client())
        else:
            break

    client_list_file = relative_path(__file__, "control/client_list.ew")

    # erase the file
    open(client_list_file, "w").close()

    with open(client_list_file, "w") as f:
        for client in client_list:
            for key in client:
                f.write(f"{key}: {client[key]}\n")
            f.write("\n")
        print("Client list file created successfully.")
    
    return True


def create_server_info():
    # Create the control_info.ew file
    # name: Fake Maze 
    # role: locknswitch 
    # class: LockNSwitch 
    # location: garage 
    # port: 12413
    # logging: True
    # log_level: INFO 
    name = input("Enter the name of the server: ")
    logging = input("Enable logging? (y/n): ")
    if logging == "y":
        logging = True
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        print("Log levels: ", end="")
        for level in log_levels:
            print(f"{level} ", end="")
        print()
        log_level = input("Enter the logging level (or press enter for default): ")
        log_level = log_level.upper()
        if log_level not in log_levels:
            if log_level != "":
                print("Invalid logging level.")
            print("Defaulting to 'INFO'")
            log_level = "INFO"
    else:
        logging = False
        log_level = "NONE"
    print("The role for the server should be a *.py file in the 'server' directory.")
    role = input("Enter the role of the server (do not include .py): ")
    r_class = input("Enter the name of the class from the role file: ")
    location = input("Enter the location of the server: ")
    port = input("Enter the port of the server(Press enter for default): ")

    if port == "":
        port = 12413
    
    server_info = {
        "name" : name,
        "role" : role,
        "class" : r_class,
        "location" : location,
        "port" : port,
        "logging" : logging,
        "log_level" : log_level
    }

    server_info_file = relative_path(__file__, "server/server_info.ew")

    with open(server_info_file, "w") as f:
        for key in server_info:
            f.write(f"{key}: {server_info[key]}\n")
        print("Server info file created successfully.")
    
    print("Server settings are as follows:")
    print(f"Name: {name}")
    print(f"Role: {role}")
    print(f"Class: {r_class}")
    print(f"Location: {location}")
    print(f"Port: {port}")
    print(f"Logging: {logging}")
    print(f"Log level: {log_level}")
    return True

def edit():
    # TODO
    print("TODO edit")
    return

def delete():
    print("WARNING: This will delete the control panel server and all associated data.")
    print("WARNING: The data will be deleted FOREVER and UNRECOVERABLE.")
    print("Are you sure you want to continue?")
    user_input = input("Enter 'I am sure' to continue: ")

    if user_input == "I am sure":
        try:
            relative_path(__file__, "control")
        except FileNotFoundError:
            print("ERROR: Server does not exist. Returning to menu.")
            return

        success = subprocess.call("rm -r control", shell=True)
        if success == 0:
            print("Server deleted successfully.")
            return
        print("Server could not be deleted.")
        return
    print("*PHEW* That was close. Server remains safe.")
    return

def create_service(type):
    # Create a file in /etc/systemd/system/ called ew-app.service
    file_path = '/etc/systemd/system/ew-app.service'
    username = subprocess.check_output("echo $USER", shell=True)


    content = f"""[Unit]
        [Unit]
        Description=Flask App
        After=network-online.target

        [Service]
        User=lodomo
        WorkingDirectory=/home/{username}/ew_local/{type}
        ExecStartPre=/bin/sleep 10
        ExecStart=/usr/bin/python3 /home/{username}/ew_local/{type}/{type}.py
        Restart=always

        [Install]
        WantedBy=multi-user.target
        """

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' created successfully.")
    except PermissionError:
        print(f"Permission denied: You need root privileges to create '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}") 

    print("Client list file created successfully.")
    return True

def exit():
    print("Thank you for using the Escape Wright Control Panel Setup Wizard.")
    print("Come back if you ever need to edit your control panel")
    return

if __name__ == "__main__":
    main()


# # Move flask-app.service file to /etc/systemd/system/
# sudo mv flask-app.service /etc/systemd/system/

# # Reload systemd daemon
# sudo systemctl daemon-reload

# # Enable and start flask-app service
# sudo systemctl enable flask-app.service
# sudo systemctl start flask-app.service