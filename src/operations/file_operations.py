import os
import shutil

import yaml

import json
from pathlib import Path
from src.utils.print_utils import log_info

def extract_stringData_secrets(yaml_file_path, output_directory):

    with open(yaml_file_path, 'r') as file:
        yaml_content = file.read()

    parsed_yaml = yaml.safe_load(yaml_content)

    if parsed_yaml.get('kind') != 'Secret':
       log_info("The file is not of kind 'Secret'. No further action will be taken.")
       return

    if 'stringData' in parsed_yaml:
        for key, value in parsed_yaml['stringData'].items():
            new_file_path = os.path.join(output_directory, f'{key}')
        
            with open(new_file_path, 'w') as new_file:
                new_file.write(value.replace('\\n', '\n'))
            current_directory = os.path.dirname(new_file_path)
            convert_to_json(new_file.name, current_directory)
    else:
        log_info("No 'stringData' found to process.")



def split_file_at_marker(input_file_path, before_marker_file_path, after_marker_file_path, marker='---'):
    write_to_before = True
    
    with open(input_file_path, 'r') as input_file, \
         open(before_marker_file_path, 'w') as before_file, \
         open(after_marker_file_path, 'w') as after_file:
        
        for line in input_file:
            if line.strip() == marker and write_to_before:
                write_to_before = False
                after_file.write(line)
                continue
                
            if write_to_before:
                before_file.write(line)
            else:
                after_file.write(line)

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
    """
    matching_directory = find_matching_directory(output_directory, service_name)
    if matching_directory:
        new_file_path = os.path.join(matching_directory, os.path.basename(file_path))
        shutil.move(file_path, new_file_path)
    else:
        log_info(f"No matching directory found for {service_name}. File remains in {output_directory}")



def group_files_by_keyword(source_dir, keywords):
    for keyword in keywords:
        keyword_dir = os.path.join(source_dir, keyword)
        if not os.path.exists(keyword_dir):
            os.makedirs(keyword_dir)

    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        if os.path.isdir(file_path):
            continue

        for keyword in keywords:
            if keyword in file_name:
                new_file_name = file_name.replace(keyword, '').replace('_','')
                dest_path = os.path.join(source_dir, keyword, new_file_name)
                shutil.move(file_path, dest_path)
                log_info(f"Moved '{file_name}' to '{dest_path}'")
                current_directory = os.path.dirname(dest_path)
                convert_to_json(dest_path, current_directory)
                if dest_path.__contains__("Secret"):
                    extract_stringData_secrets(dest_path, current_directory)
                break

def clear_directory(directory_path):
    """
    Deletes all the contents of a specified directory without removing the directory itself.
    """
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log_info(f"Failed to delete {file_path}. Reason: {e}")


def ensure_directory_exists(directory_path):
    """
    Checks if a directory exists, and if not, creates it.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        log_info(f"Directory created: {directory_path}")
    else:
        log_info(f"Directory already exists: {directory_path}")


def convert_to_json(filename, dirpath):
    yaml_file_path = Path(dirpath) / filename
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
                
    json_dir = Path(dirpath) / 'json'
    json_dir.mkdir(exist_ok=True)
                
    json_content = json.dumps(yaml_content, indent=4)
    json_file_path = json_dir / f"{yaml_file_path.stem}.json"
                
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_content)
    return yaml_file_path,json_file_path