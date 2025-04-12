from dagster import Definitions
from orchestration.video_pipeline import (
    load_video_plan,
    generate_scene_visuals,
    generate_scene_voiceovers,
    compose_videos,
)

defs = Definitions(
    assets=[
        load_video_plan,
        generate_scene_visuals,
        generate_scene_voiceovers,
        compose_videos,
    ]
)