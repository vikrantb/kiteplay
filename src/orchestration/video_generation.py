from dagster import op, job
from src.assets.script_generation import generate_script
from src.assets.image_generation import generate_image
from src.assets.scene_generation import generate_video
from src.assets.video_composition import merge_video_audio
from src.orchestration.publishing import publish_video

# 📝 Script Generation
@op
def script_op():
    return generate_script("Write a 30-second Holi celebration video script.")

# 🎬 Video Scene Generation
@op
def video_op(script):
    return generate_video(script)

# 🖼️ Image Generation (Fallback)
@op
def image_op(script):
    return generate_image(script)

# 🎥 Merge Video + Audio
@op
def merge_op(video_file):
    return merge_video_audio(video_file, "voiceover.mp3")

# 🚀 Publish Video
@op
def publish_op(final_video):
    return publish_video(final_video, "🎨 Holi celebrations! #Holi2024")

# 🎯 Pipeline Definition
@job
def ai_video_pipeline():
    script = script_op()
    video = video_op(script)
    final_video = merge_op(video)
    publish_op(final_video)