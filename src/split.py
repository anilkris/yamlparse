import yaml
import os
import shutil
import get_manifest
import cert
import extract
import values


current_script_path = os.path.abspath(__file__)


src_directory = os.path.dirname(current_script_path)


project_root_directory = os.path.dirname(src_directory)


input_directory = os.path.join(project_root_directory, 'input')


output_directory = os.path.join(project_root_directory, 'output')


os.makedirs(output_directory, exist_ok=True)


input_file_path = os.path.join(input_directory, 'dryrun.yaml')
output_dir =os.path.join(output_directory, 'dryrun_output')

before_marker_file_path = os.path.join(output_directory,'user_and_computed_values.yaml')
only_manifests_file_path = os.path.join(output_directory,'manifests.yaml')


start_marker = 'USER-SUPPLIED VALUES:'
mid_marker = 'COMPUTED VALUES:'
end_marker = None  # Optional: use None if you want to copy until EOF
# Define output file paths
first_section_file_path = os.path.join(output_directory,'user_supplied_values.yaml')
second_section_file_path = os.path.join(output_directory, 'computed_values.yaml')

def split_helm_output(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as file:
        docs = yaml.safe_load_all(file)

        for doc in docs:
            if doc is None:
                continue

            kind = doc.get('kind', 'UnknownKind')
            name = doc['metadata']['name']
            file_name = f"{kind}_{name}.yaml"

            with open(os.path.join(output_dir, file_name), 'w') as outfile:
                yaml.dump(doc, outfile, default_flow_style=False)




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


def find_folder_name_from_yaml_files(directory_path):
    folder_names = []

    for file_name in os.listdir(directory_path):
        if file_name.startswith('Pod_') and file_name.endswith('-test-connection.yaml'):
            clean_name = file_name[len('Pod_'):-len('-test-connection.yaml')]
            folder_names.append(clean_name)

    return folder_names

get_manifest.split_file_at_marker(input_file_path, before_marker_file_path, only_manifests_file_path)
split_helm_output(only_manifests_file_path, output_dir)
keywords = find_folder_name_from_yaml_files(output_dir)
group_files_by_keyword(output_dir, keywords)


# certificates = cert.extract_certificates_from_file(input_file_path)
# cert.printcerts(certificates)

extract.extract_and_save_content(before_marker_file_path, start_marker, mid_marker, first_section_file_path,second_section_file_path, end_marker)


yaml_files = [first_section_file_path,second_section_file_path]

values_output_directory = os.path.join(output_directory, 'dryrun_output')
values.parse_yaml_and_create_files(yaml_files, values_output_directory)