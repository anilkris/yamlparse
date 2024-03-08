import yaml
def extract_and_save_content(input_file_path, start_marker, mid_marker,  first_section_file_path,second_section_file_path, end_marker=None,):
    """
    Extracts content from an input file between two markers and from a middle marker to EOF.
    Writes the content to two different files.

    :param input_file_path: Path to the input file
    :param start_marker: The starting marker for the first section to extract
    :param mid_marker: The middle marker, end of the first section and start of the second section
    :param end_marker: The end marker for the second section, if None, goes to EOF
    """
    # Initialize strings to hold the extracted content
    first_section = ""
    second_section = ""

    # Flags to track whether we're between the desired markers
    is_first_section = False
    is_second_section = False

    # Read the input file
    with open(input_file_path, 'r') as file:
        for line in file:
            # Check for the start of the first section
            if start_marker in line:
                is_first_section = True
                continue  # Skip the line with the start marker itself

            # Check for the end of the first section and start of the second section
            if mid_marker in line:
                is_first_section = False
                is_second_section = True
                continue  # Skip the line with the mid marker itself
            
            # If an end marker is provided, check for it
            if end_marker and end_marker in line:
                is_second_section = False
                break  # Stop reading the file if end marker is found

            # Append line to the appropriate section based on flags
            if is_first_section:
                first_section += line
            elif is_second_section:
                second_section += line

 

    # Write the first section to its file
    with open(first_section_file_path, 'w') as file:
        file.write(first_section)

    # Write the second section to its file
    with open(second_section_file_path, 'w') as file:
        file.write(second_section)

    print(f"First section saved to: {first_section_file_path}")
    print(f"Second section saved to: {second_section_file_path}")

# Example usage
