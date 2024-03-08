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

input_file_path = 'dryrun.yaml'


