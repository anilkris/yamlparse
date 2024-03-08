import os

def get_project_directories():
    current_script_path = os.path.abspath(__file__)
    src_directory = os.path.dirname(current_script_path)
    project_root_directory = os.path.dirname(src_directory)
    input_directory = os.path.join(project_root_directory, 'input')
    output_directory = os.path.join(project_root_directory, 'output')
    return input_directory, output_directory
