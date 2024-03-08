import os
from src.operations.file_operations import clear_directory, split_file_at_marker, group_files_by_keyword
from src.operations.yaml_operations import parse_yaml_and_create_files, split_helm_output,find_folder_name_from_yaml_files,extract_and_save_content
from src.operations.cert_operations import extract_certificates_from_file, printcerts
from src.utils.path_utils import get_resource_directories
from src.utils.print_utils import print_message, log_info, log_error

def main():
    try:
        # Set up directories
        input_directory, output_directory = get_resource_directories()
        print_message("Starting the application...")

        # Define paths for input and output files based on the project directories
        input_file_path = os.path.join(input_directory, 'demo.yaml')
        output_dir = os.path.join(output_directory, 'dryrun_output')

        clear_directory(output_directory)

        user_and_computed_values_file_path = os.path.join(output_directory,'user_and_computed_values.yaml')
        only_manifests_file_path = os.path.join(output_directory,'manifests.yaml')


        start_marker = 'USER-SUPPLIED VALUES:'
        mid_marker = 'COMPUTED VALUES:'
        end_marker = None
        first_section_file_path = os.path.join(output_directory,'user_supplied_values.yaml')
        second_section_file_path = os.path.join(output_directory, 'computed_values.yaml')

        # Perform operations
        # Yaml operations 
        split_file_at_marker(input_file_path, user_and_computed_values_file_path, only_manifests_file_path)
        split_helm_output(only_manifests_file_path, output_dir)
        print_message("Helm output split successfully.")

        keywords = find_folder_name_from_yaml_files(output_dir)

        group_files_by_keyword(output_dir, keywords)

        extract_and_save_content(user_and_computed_values_file_path, start_marker, mid_marker, first_section_file_path,second_section_file_path, end_marker)

        yaml_files = [first_section_file_path,second_section_file_path]

        parse_yaml_and_create_files(yaml_files, output_dir)

        # Extract and print certificates (as an example)
        certificates = extract_certificates_from_file(input_file_path)
        if certificates:
            printcerts(certificates)
            print_message("Certificates processed.")
        else:
            print_message("No certificates found.")

        # More operations can be added here following the similar pattern

        log_info("Application executed successfully.")
    except Exception as e:
        log_error(f"An error occurred: {str(e)}")
        print_message("An error occurred, check the logs for details.")

if __name__ == "__main__":
    main()
