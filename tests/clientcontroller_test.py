from escapewright.escapiclientcontroller import EscapiClientController
import os

def main():
    print("Current Working Directory:", os.getcwd())
    filename = "./tests/client_list.ew"
    client_controller = EscapiClientController(filename)
    client_controller.print_all_clients()

if __name__ == '__main__':
    main()