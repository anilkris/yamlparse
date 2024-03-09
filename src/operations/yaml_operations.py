import os
import yaml

from src.operations.file_operations import move_file_to_matching_directory
from src.utils.print_utils import log_info

availableServices=[]
def split_helm_output(input_file, output_dir):
    """
    Splits a Helm output file into separate YAML files for each Kubernetes resource.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as file:
        docs = yaml.safe_load_all(file)
        for doc in docs:
            if doc is None:
                continue
            kind = doc.get('kind', 'UnknownKind')
            name = doc['metadata']['name']
            # if(kind == 'Secret') or (kind == 'ConfigMap') or (kind == 'Service'):
            addNameToAvailableServices(name)
            file_name = f"{kind}_{name}.yaml"
            with open(os.path.join(output_dir, file_name), 'w') as outfile:
                yaml.dump(doc, outfile, default_flow_style=False)

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
        log_info(f"File created for {service}: {output_file_path}")
        move_file_to_matching_directory(output_file_path, service, output_directory)

def filter_sensitive_values(service_values, keys_to_remove=['certificate', 'key', 'jwt']):
    """
    Recursively filters out sensitive values from a dictionary based on the specified keys.
    """
    def replace_sensitive_values(data, placeholder='[SENSITIVE]'):
        if isinstance(data, dict):
            return {key: replace_sensitive_values(value, key) if key not in keys_to_remove else placeholder for key, value in data.items()}
        elif isinstance(data, list):
            return [replace_sensitive_values(item) for item in data]
        else:
            return data
    return replace_sensitive_values(service_values)



def addNameToAvailableServices(name):
    if isinstance(name, str ) and name not in availableServices:
        availableServices.append(name)
    else:
        return
    


def getAvailableServices(): 
    return availableServices


def extract_and_save_content(input_file_path, start_marker, mid_marker, first_section_file_path, second_section_file_path, end_marker=None):
    """
    Extracts content from the input file based on start and mid markers, and optionally an end marker.
    Saves the extracted content into two separate files.
    """
    first_section = ""
    second_section = ""
    is_first_section = False
    is_second_section = False

    with open(input_file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                is_first_section = True
                continue

            if mid_marker in line:
                is_first_section = False
                is_second_section = True
                continue
            
            if end_marker and end_marker in line:
                is_second_section = False
                break

            if is_first_section:
                first_section += line
            elif is_second_section:
                second_section += line

    with open(first_section_file_path, 'w') as file:
        file.write(first_section)

    with open(second_section_file_path, 'w') as file:
        file.write(second_section)

    return first_section_file_path, second_section_file_path

