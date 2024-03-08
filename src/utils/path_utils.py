import os

def get_resource_directories():
    # This line calculates the path to the directory containing 'path_utils.py'
    current_file_path = os.path.abspath(__file__)
    # Moves up three levels to get the project root directory
    project_root_directory = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    resources_directory = os.path.join(project_root_directory, 'resources')
    input_directory = os.path.join(resources_directory, 'input')
    output_directory = os.path.join(resources_directory, 'output')
    return input_directory, output_directory
