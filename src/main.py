import os
from src.operations.file_operations import clear_directory, ensure_directory_exists,  split_file_at_marker, group_files_by_keyword
from src.operations.yaml_operations import getAvailableServices, parse_yaml_and_create_files, split_helm_output,extract_and_save_content
from src.operations.cert_operations import extract_certificates_from_file, printcerts
from src.utils.path_utils import get_resource_directories
from src.utils.print_utils import delete_logfile, print_message, log_info, log_error

def main():
    try:

        print_message("Application started...")
        input_directory, output_directory = get_resource_directories() 

        input_file_path = os.path.join(input_directory, 'input.yaml')
        output_dir = os.path.join(output_directory, 'dryrun_output')

        ensure_directory_exists(output_directory)

        delete_logfile()
        clear_directory(output_directory)

        user_and_computed_values_file_path = os.path.join(output_directory,'user_and_computed_values.yaml')
        only_manifests_file_path = os.path.join(output_directory,'manifests.yaml')


        start_marker = 'USER-SUPPLIED VALUES:'
        mid_marker = 'COMPUTED VALUES:'
        end_marker = None
        first_section_file_path = os.path.join(output_directory,'user_supplied_values.yaml')
        second_section_file_path = os.path.join(output_directory, 'computed_values.yaml')

        split_file_at_marker(input_file_path, user_and_computed_values_file_path, only_manifests_file_path)

        split_helm_output(only_manifests_file_path, output_dir)
        names =  getAvailableServices()

        group_files_by_keyword(output_dir, names)

        extract_and_save_content(user_and_computed_values_file_path, start_marker, mid_marker, first_section_file_path,second_section_file_path, end_marker)

        yaml_files = [first_section_file_path,second_section_file_path]
        parse_yaml_and_create_files(yaml_files, output_dir)

        certificates = extract_certificates_from_file(input_file_path)
        if certificates:
            printcerts(certificates)
            log_info("Certificates processed.")
        else:
            log_info("No certificates found.")

        print_message("Application executed successfully.\nOuput: "+ output_dir)
    except Exception as e:
        log_error(f"An error occurred: {str(e)}")
        print_message("An error occurred, check the logs for details.")

if __name__ == "__main__":
    main()
