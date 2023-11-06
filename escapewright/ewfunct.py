import importlib
import os

def import_at_runtime(module_name):
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
        return None

def ew_to_dict(filename):
    dict = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            key, value = line.split(':')
            dict[key.strip()] = value.strip()
    return dict
