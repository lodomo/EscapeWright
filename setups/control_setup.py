################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Create and setup the control server.
#     Updated: 07 NOV 2023
# Description: Wizard to create a control panel server.
#              
################################################################################

import os
import shutil
from importlib import util
import subprocess


from escapewright.ewfunct import relative_path

def main():
    welcome()
    while menu():
        pass
    exit()
    return

def welcome():
    print(" ______  _____  _____          _____  ______    ")
    print("|  ____|/ ____|/ ____|   /\   |  __ \|  ____|   ")
    print("| |__  | (___ | |       /  \  | |__) | |__      ")
    print("|  __|  \___ \| |      / /\ \ |  ___/|  __|     ")
    print("| |____ ____) | |____ / ____ \| |    | |____    ")
    print("|______|_____/_\_____/_/__ _\_\_|_   |______|__ ")
    print("\ \        / /  __ \|_   _/ ____| |  | |__   __|")
    print(" \ \  /\  / /| |__) | | || |  __| |__| |  | |   ")
    print("  \ \/  \/ / |  _  /  | || | |_ |  __  |  | |   ")
    print("   \  /\  /  | | \ \ _| || |__| | |  | |  | |   ")
    print("    \/  \/   |_|  \_\_____\_____|_|  |_|  |_| ")
    print("Welcome to the Escape Wright Control Panel Setup Wizard!")

def menu():
    EXIT = 4
    print("Menu:")
    print("1. Create a new control panel server")
    print("2. Edit an existing control panel server")
    print("3. Delete an existing control panel server")
    print("4. Exit")
    user_input = str(input("Select an option: "))

    menu_cases = {
        "1" : create,
        "2" : edit,
        "3" : delete
    }

    if user_input == str(EXIT):
        return False

    if user_input in menu_cases:
        menu_cases[user_input]()
    else:
        print("Invalid input.")
    return again()

def again():
    user_input = input("Would you like to do something else? (y/n): ")
    if user_input == "y":
        print()
        return True
    elif user_input == "n":
        print()
        return False
    else:
        print("Invalid input. Returning to menu.")
        print()
    return True

def create():
    # Create a new control panel server
    if check_if_exists(): return
    if not clone_directory("control"): return
    create_server_info()
    return

def check_if_exists():
    try:
        relative_path(__file__, "control")
        print("ERROR: A control panel server already exists.")
        print("Choose 'Edit an existing control panel server' from the menu to edit the server.")
        return True
    except FileNotFoundError:
        return False 


def clone_directory(folder):
    # Find the 'escapewright' module directory
    module_spec = util.find_spec("escapewright")
    if module_spec is not None and module_spec.origin is not None:
        escapewright_path = os.path.dirname(module_spec.origin)
        templates_control_path = os.path.join(escapewright_path, 'templates', folder)
        
        # Check if the 'templates/control' directory exists
        if os.path.isdir(templates_control_path):
            # Clone 'templates/control' to the current directory
            destination_path = os.path.join(os.getcwd(), 'control')
            shutil.copytree(templates_control_path, destination_path)
            print(f"'control' template has been cloned to the current directory: {destination_path}")
            return True
        else:
            print(f"The 'control template' directory does not exist in the 'escapewright' library at {templates_control_path}")
            print(f"Reinstall the escapewright library.")
            return False
    else:
        print("The 'escapewright' module is not installed or could not be found.")
    return False

def create_server_info():
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


def edit():
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

def exit():
    print("Thank you for using the Escape Wright Control Panel Setup Wizard.")
    print("Come back if you ever need to edit your control panel")
    return

if __name__ == "__main__":
    main()