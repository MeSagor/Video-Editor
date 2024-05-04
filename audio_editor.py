from moviepy.editor import VideoFileClip, AudioFileClip

video_path = 'new_resulation/mamun3.mp4'
external_audio_path = 'refine2.wav'
output_audio_path = 'output_audio2.wav'
output_video_path = 'refine_video2.mp4'

video_clip = VideoFileClip(video_path)

# audio = video_clip.audio
# audio.write_audiofile(output_audio_path)

external_audio_clip = AudioFileClip(external_audio_path)
video_with_audio = video_clip.set_audio(external_audio_clip)
video_with_audio.write_videofile(output_video_path, codec='libx264', audio_codec='aac')