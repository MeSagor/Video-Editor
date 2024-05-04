import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

# Function to extract audio from a video using ffmpeg
def make_audio(input_video, output_audio):
    command = f'ffmpeg -i {input_video} -vn -acodec pcm_s16le -ar 44100 -ac 2 {output_audio}'
    os.system(command)

# Function to remove non-speaking segments from audio using a threshold
def make_non_speaking_segment_gone(threshold, window_time, sample_rate, audio_waveform):
    window_size = int(window_time * sample_rate)
    mask = np.zeros_like(audio_waveform)
    
    for i in range(0, len(audio_waveform) - window_size, window_size):
        window = audio_waveform[i: i + window_size]
        if np.all(window <= threshold):
            mask[i: i + window_size] = 0
        else:
            mask[i: i + window_size] = 1
    return mask

# Function to detect speaking segments in audio
def detect_speaking_segments(audio_waveform, sample_rate):
    speaking_segments = []
    is_speaking = False

    for i, amplitude in enumerate(audio_waveform):
        if amplitude > 0:
            if not is_speaking:
                start_time = i / sample_rate
                is_speaking = True
        else:
            if is_speaking:
                end_time = i / sample_rate
                speaking_segments.append((start_time, end_time))
                is_speaking = False

    # Add a final speaking segment if the audio ends with speech
    if is_speaking:
        end_time = (len(audio_waveform) - 1) / sample_rate
        speaking_segments.append((start_time, end_time))

    return speaking_segments

def do_plotting(audio, audio_waveform):
    time = librosa.times_like(audio)
    plt.figure(figsize=(12, 7))
    plt.subplot(211)
    plt.plot(time, np.abs(audio) / np.max(np.abs(audio)), linewidth=0.5)
    plt.plot(time, audio_waveform, linewidth=1.5)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Original Audio Waveform')
    plt.grid(True)
    plt.legend(['Original Audio', 'Filter Mask'])
    plt.subplot(212)
    plt.plot(time, np.abs(audio) * audio_waveform, linewidth=0.5)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Speaking Audio Waveform')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to perform video clipping based on speaking segments
def do_video_clipping(speaking_segments, output_directory, general_file_name, video, video_number, padding_time):
    os.makedirs(output_directory, exist_ok=True)
    for i, (start_time, end_time) in enumerate(speaking_segments):
        # if i == 10:
        #     break
        start_time = max(start_time - padding_time, 0)
        end_time = min(end_time + padding_time, video.duration)
        output_video_path = os.path.join(output_directory, f'{general_file_name}{i+video_number}.mp4')
        subclip = video.subclip(start_time, end_time)
        subclip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')




# Perameters
input_video_path = 'refine_video2.mp4'
output_audio_path = 'audio.wav'
output_directory = 'output_clips/'
# output_directory = 'word_clips/'
output_general_file_name = 'clip'
video_number = 30
padding_time = 0.25
threshold = 0.06
window_time = 0.35

# Load the video
video = VideoFileClip(input_video_path)
print(f'Video Size: {video.size}')

# Extract audio from the video
make_audio(input_video=input_video_path, output_audio=output_audio_path)

# Load the audio from the extracted WAV file
audio, sample_rate = librosa.load(output_audio_path)
os.remove(output_audio_path)
audio_waveform = np.abs(audio)
print(f'Sampling rate: {sample_rate}')

# Apply thresholding to remove non-speaking segments
audio_waveform = make_non_speaking_segment_gone(threshold, window_time, sample_rate, audio_waveform)

# Detect speaking segments in the audio
speaking_segments = detect_speaking_segments(audio_waveform, sample_rate)
print(speaking_segments)

# Plot the audio wave-form
# do_plotting(audio, audio_waveform)

# Perform video clipping based on speaking segments
do_video_clipping(speaking_segments, output_directory, output_general_file_name, video, video_number, padding_time)
