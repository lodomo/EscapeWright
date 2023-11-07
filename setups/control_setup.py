################################################################################
#
#      Author: Lodomo.dev (Lorenzo D. Moon)
#     Purpose: Create and setup the control server.
#     Updated: 07 NOV 2023
# Description: Wizard to create a control panel server.
#              
################################################################################

import subprocess

from escapewright.ewfunct import relative_path

def main():
    welcome()
    menu()
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
    print("Menu:")
    print("1. Create a new control panel server")
    print("2. Edit an existing control panel server")
    print("3. Delete an existing control panel server")
    print("4. Exit")
    user_input = str(input("Select an option: "))

    menu_cases = {
        "1" : create,
        "2" : edit,
        "3" : delete,
        "4" : exit
    }

    menu_cases[user_input]()
    return

def create():
    return

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
    return

if __name__ == "__main__":
    main()