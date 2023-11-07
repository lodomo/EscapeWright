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
            if line.startswith('#') or line == '':
                continue
            key, value = line.split(':')
            dict[key.strip()] = value.strip()
    return dict

def relative_path(script, file_or_directory):
    # Return the path to a file or directory relative to the script
    # script should be __file__
    # Generate the absolute path
    abs_path = os.path.join(os.path.dirname(os.path.abspath(script)), file_or_directory)
    
    # Check if the path exists
    if os.path.exists(abs_path):
        return abs_path
    else:
        raise FileNotFoundError(f"The path {abs_path} does not exist.")