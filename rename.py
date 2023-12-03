import os

new_general_name = 'clip'

folder_path = os.getcwd()
folder_path = os.path.join(folder_path, 'output_clips')
file_list = os.listdir(folder_path)

# sort the list of filenames according to the number within their names


def sort_key(filename):
    try:
        number = int(''.join(filter(str.isdigit, filename)))
        return number
    except ValueError:
        return float('inf')


file_list = sorted(file_list, key=sort_key)
# print(file_list)

for i, old_filename in enumerate(file_list):
    if old_filename == '.DS_Store':
        continue
    new_filename = f'{new_general_name}{i}.mp4'
    old_filepath = os.path.join(folder_path, old_filename)
    new_filepath = os.path.join(folder_path, new_filename)
    os.rename(old_filepath, new_filepath)
    print(f'Renamed: {old_filename} -> {new_filename}')
