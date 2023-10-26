# Import escape from escapewright from the sibling folder.
from escapewright import escapi

# def __init__(self, name, ip_address, port, location):
test = escapi.Client(1, "192.168.0100", 2413, 1)

for error in test.errors:
    print("Error Found: " + error)

input("Press enter to quit")