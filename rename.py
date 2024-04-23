import os
import shutil

new_general_name = 'clip'

source_folder_path = os.getcwd()
source_folder_path = os.path.join(source_folder_path, 'output_clips')
destination_folder_path = os.getcwd()
destination_folder_path = os.path.join(destination_folder_path, 'renamed_output_clips')
file_list = os.listdir(source_folder_path)

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# sort the list of filenames according to the number within their names
def sort_key(filename):
    try:
        number = int(''.join(filter(str.isdigit, filename)))
        return number
    except ValueError:
        return float('inf')


file_list = sorted(file_list, key=sort_key)
# print(file_list)



count = 0

for i, old_filename in enumerate(file_list):
    if old_filename == '.DS_Store':
        continue
    new_filename = f'{new_general_name}{i + count}.mp4'
    old_filepath = os.path.join(source_folder_path, old_filename)
    new_filepath = os.path.join(destination_folder_path, new_filename)
    shutil.copy(old_filepath, new_filepath)
    print(f'Copied and Renamed: {old_filename} -> {new_filename}')
