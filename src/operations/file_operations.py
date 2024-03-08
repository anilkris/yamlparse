import os
import shutil


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
        print(f"Moved {file_path} to {new_file_path}")
    else:
        print(f"No matching directory found for {service_name}. File remains in {output_directory}")



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
                print(f"Moved '{file_name}' to '{dest_path}'")
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
            print(f"Failed to delete {file_path}. Reason: {e}")

def ensure_directory_exists(directory_path):
    """
    Checks if a directory exists, and if not, creates it.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")