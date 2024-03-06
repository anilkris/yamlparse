import yaml
import os
import shutil

input_file = 'helm_output.yaml'  
output_dir = 'dryrun_output' 


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



split_helm_output(input_file, output_dir)
keywords = find_folder_name_from_yaml_files(output_dir)
group_files_by_keyword(output_dir, keywords)
