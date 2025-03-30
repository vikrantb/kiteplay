import os

def merge_video_audio(video_file, audio_file, output_file="final_video.mp4"):
    """Merges video and audio using FFmpeg."""
    os.system(f"ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac {output_file}")
    return output_file

if __name__ == "__main__":
    print(merge_video_audio("video.mp4", "voiceover.mp3"))