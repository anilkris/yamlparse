import os
import shutil
import yaml

def replace_sensitive_values(data, keys_to_replace, placeholder='sensitive data'):
    if isinstance(data, dict):
        return {
            key: replace_sensitive_values(value, keys_to_replace, key)
            if key not in keys_to_replace else key
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [replace_sensitive_values(item, keys_to_replace, placeholder) for item in data]
    else:
        return data

def filter_sensitive_values(service_values):
    keys_to_remove = ['certificate', 'key', 'roleRightsMap']
    return replace_sensitive_values(service_values, keys_to_remove)
def find_matching_directory(base_directory, target_name):
    """
    Searches for a directory within base_directory where target_name is part of the directory name.

    :param base_directory: The directory to search within.
    :param target_name: The name (or part of the name) of the directory to search for.
    :return: Path to the first matching directory found or None if not found.
    """
    for root, dirs, _ in os.walk(base_directory):
        for dir_name in dirs:
            if target_name in dir_name:
                return os.path.join(root, dir_name)
    return None

def move_file_to_matching_directory(file_path, service_name, output_directory):
    """
    Moves the file to a directory within output_directory if the service name is part of the directory name.

    :param file_path: The path to the file to move.
    :param service_name: The name of the service, used to find matching directory names.
    :param output_directory: The base directory to search for a matching directory.
    """
    matching_directory = find_matching_directory(output_directory, service_name)
    if matching_directory:
        # Calculate the new path within the matching directory
        new_file_path = os.path.join(matching_directory, os.path.basename(file_path))
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_path} to {new_file_path}")
    else:
        print(f"No matching directory found for {service_name}. File remains in {output_directory}")


def parse_yaml_and_create_files(yaml_files, output_directory):
 
    os.makedirs(output_directory, exist_ok=True)
    
    services = {}

    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            for service, values in data.items():
                filtered_values = filter_sensitive_values(values)
                services[service] = filtered_values

    for service, values in services.items():
        output_file_path = os.path.join(output_directory, f"{service}_values.yaml")
        with open(output_file_path, 'w') as file:
            yaml.dump({service: values}, file, default_flow_style=False)
        print(f"File created for {service}: {output_file_path}")
        move_file_to_matching_directory(output_file_path, service, output_directory)
 


