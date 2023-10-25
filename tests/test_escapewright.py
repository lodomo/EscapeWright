from escapewright import escapi 

# def __init__(self, name, ip_address, port, location):
test = escapi.Client(1, "192.168.0100", 2413, 1)

# # Print all members
# print("All Members:")
# print(test.name)
# print(test.ip)
# print(test.location)
# print(test.port)
# print(test.validate())
# print(test.reachable)
# print(test.status)
# print(test.status_was)
# print(test.address)

for error in test.errors:
    print("Error Found: " + error)

input("Press enter to quit")