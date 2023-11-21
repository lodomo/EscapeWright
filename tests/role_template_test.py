from escapewright.role_template import RoleTemplate

def main():
    print("Role Template Test")
    role = RoleTemplate()
    print(f"Observer: {role.observer}")
    print(f"Status: {role.status}")
    print(f"Running: {role.running}")
    print(f"Logger: {role.logger}")
    print(f"Triggers: {role.triggers.keys()}") # Updated from Unique
    role.load()
    print(f"After Load Status: {role.status}")
    role.start()
    print(f"After Start Status: {role.status}")
    print(f"reset {role.reset()}")
    print(f"After Reset Status: {role.status}")
    role.stop()
    print(f"After Stop Status: {role.status}")
    role.bypass()
    print(f"After Bypass Status: {role.status}")
    return

if __name__ == "__main__":
    main()