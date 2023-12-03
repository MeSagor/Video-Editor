import os


new_general_name = 'clip'
output_folder_path = 'new_resulation'
input_folder_path = os.path.join(os.getcwd(), 'output_clips')
file_list = os.listdir(input_folder_path)

# sort the list of filenames according to the number within their names
def sort_key(filename):
    try:
        number = int(''.join(filter(str.isdigit, filename)))
        return number
    except ValueError:
        return float('inf')

file_list = sorted(file_list, key=sort_key)
# print(file_list)

os.makedirs(output_folder_path, exist_ok=True)
for i, filename in enumerate(file_list):
    if filename == '.DS_Store':
        continue
    output_video_name = f'{new_general_name}{i}.mp4'
    input_video_path = os.path.join(input_folder_path, filename)
    command = f'ffmpeg -i {input_video_path} -vf scale=320:320 {output_video_name}'
    os.system(command)
    command = f'mv {new_general_name}{i}.mp4 ./{output_folder_path}'
    os.system(command)
    print(f'resulation-> {filename}')
