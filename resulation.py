import os

output_folder_path = 'new_resulation'
input_folder_path = os.path.join(os.getcwd(), 'raw_videos')
file_list = os.listdir(input_folder_path)

os.makedirs(output_folder_path, exist_ok=True)

for i, filename in enumerate(file_list):
    if filename.endswith('.mp4'):
        input_file = os.path.join(input_folder_path, filename)
        output_file = os.path.join(output_folder_path, filename)
        command = f'ffmpeg -i {input_file} -vf scale=320:320 {output_file}'
        os.system(command)
        print(f'{output_file} is created.')
