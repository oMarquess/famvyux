import os
import json

def combine_json_files(directory_path, output_file='data.json'):
    """
    Reads all JSON files in the given directory and combines them into a single JSON file.
    """
    combined_data = []
    
    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.append(data)
            
    # Write the combined data to a file
    with open(output_file, 'w') as file:
        json.dump(combined_data, file, indent=4)
        print(f"Wrote {output_file}")

combine_json_files('C:\Users\edakw\OneDrive\Not important pre(2023)\Desktop\famvyux\famvyux\IMBD')